/* -*- c++ -*- */
/*
 * Copyright 2015 <Nikos Kargas (nkargas@isc.tuc.gr)>.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <gnuradio/prefs.h>
#include <gnuradio/math.h>
#include <cmath>
#include <sys/time.h>
#include "tag_decoder_impl.h"

namespace gr {
  namespace rfid {

    tag_decoder::sptr
    tag_decoder::make(int sample_rate)
    {

      // std::vector<int> output_sizes;
      // output_sizes.push_back(sizeof(float));
      // //output_sizes.push_back(sizeof(char));
      // output_sizes.push_back(sizeof(float));

      return gnuradio::get_initial_sptr
        (new tag_decoder_impl(sample_rate));
    }

    /*
     * The private constructor
     */
    tag_decoder_impl::tag_decoder_impl(int sample_rate)
      : gr::block("tag_decoder",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(float) )),
              s_rate(sample_rate)
    {


      char_bits = (char *) malloc( sizeof(char) * 128);

      n_samples_TAG_BIT = TAG_BIT_D * s_rate / pow(10,6);
      // GR_LOG_INFO(d_logger, "Number of samples of Tag bit : " + std::to_string(n_samples_TAG_BIT));
  }

    /*
     * Our virtual destructor.
     */
    tag_decoder_impl::~tag_decoder_impl()
    {

    }

    void
    tag_decoder_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        ninput_items_required[0] = noutput_items;
    }

    int find_offset(const gr_complex * in)
    {
      float max = 0;
      int offset = -1;
      for(int i = 0; i < 5; i ++){
        float sum = 0;
        for (int j = i; j < i + 10; j ++){
          sum += std::abs(in[j]);
        }

        if(sum > max){
          max = sum;
          offset = i;
        }
      }
      
      return offset;
    }

    float avg_fm0(const gr_complex * in, int offset)
    {
      float sum = 0;
      int count = 40;
      for(int i = offset; i < count + offset; i ++)
      {
        sum += std::abs(in[i]);
      }
      float avg = sum / count;
      return avg;
    }

    int tag_decoder_impl::tag_sync(const gr_complex * in , int size)
    {
      int max_index = 0;
      float max = 0.1,corr;
      gr_complex corr2;

      // Do not have to check entire vector (not optimal)
      for (int i=0; i < 1.5 * n_samples_TAG_BIT ; i++)
      {
        corr2 = gr_complex(0,0);
        corr = 0;
        // sync after matched filter (equivalent)
        for (int j = 0; j < 2 * TAG_PREAMBLE_BITS; j ++)
        {
          corr2 = corr2 + in[ (int) (i+j*n_samples_TAG_BIT/2) ] * gr_complex(TAG_PREAMBLE[j],0);
        }
        corr = std::norm(corr2);
        if (corr > max)
        {
          max = corr;
          max_index = i;
        }
      }

       // Preamble ({1,1,-1,1,-1,-1,1,-1,-1,-1,1,1} 1 2 4 7 11 12))
      h_est = (in[max_index] + in[ (int) (max_index + n_samples_TAG_BIT/2) ] + in[ (int) (max_index + 3*n_samples_TAG_BIT/2) ] + in[ (int) (max_index + 6*n_samples_TAG_BIT/2)] + in[(int) (max_index + 10*n_samples_TAG_BIT/2) ] + in[ (int) (max_index + 11*n_samples_TAG_BIT/2)])/std::complex<float>(6,0);


      // Shifted received waveform by n_samples_TAG_BIT/2
      max_index = max_index + TAG_PREAMBLE_BITS * n_samples_TAG_BIT;
      return max_index;
    }




    std::vector<float>  tag_decoder_impl::tag_detection_RN16(std::vector<gr_complex> & RN16_samples_complex)
    {
      // detection + differential decoder (since Tag uses FM0)
      std::vector<float> tag_bits,dist;
      float result;
      int prev = 1,index_T=0;

      for (int j = 0; j < RN16_samples_complex.size()/2 ; j ++ )
      {
        result = std::real( (RN16_samples_complex[2*j] - RN16_samples_complex[2*j+1])*std::conj(h_est));

        if (result>0){
          if (prev == 1)
            tag_bits.push_back(0);
          else
            tag_bits.push_back(1);
          prev = 1;
        }
        else
        {
          if (prev == -1)
            tag_bits.push_back(0);
          else
            tag_bits.push_back(1);
          prev = -1;
        }
      }
      return tag_bits;
    }


    std::vector<float>  tag_decoder_impl::tag_detection_EPC(std::vector<gr_complex> & EPC_samples_complex, int index)
    {
      std::vector<float> tag_bits,dist;
      float result=0;
      int prev = 1;

      int number_steps = 20;
      float min_val = n_samples_TAG_BIT/2.0 -  n_samples_TAG_BIT/2.0/100, max_val = n_samples_TAG_BIT/2.0 +  n_samples_TAG_BIT/2.0/100;

      std::vector<float> energy;

      energy.resize(number_steps);
      for (int t = 0; t <number_steps; t++)
      {
        for (int i =0; i <256; i++)
        {
          energy[t]+= reader_state->magn_squared_samples[(int) (i * (min_val + t*(max_val-min_val)/(number_steps-1)) + index)];
        }

      }
      int index_T = std::distance(energy.begin(), std::max_element(energy.begin(), energy.end()));
      float T =  min_val + index_T*(max_val-min_val)/(number_steps-1);

      // T estimated
      T_global = T;

      for (int j = 0; j < 128 ; j ++ )
      {
        result = std::real((EPC_samples_complex[ (int) (j*(2*T) + index) ] - EPC_samples_complex[ (int) (j*2*T + T + index) ])*std::conj(h_est) );


         if (result>0){
          if (prev == 1)
            tag_bits.push_back(0);
          else
            tag_bits.push_back(1);
          prev = 1;
        }
        else
        {
          if (prev == -1)
            tag_bits.push_back(0);
          else
            tag_bits.push_back(1);
          prev = -1;
        }
      }
      return tag_bits;
    }


    int
    tag_decoder_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {


      const gr_complex *in = (const  gr_complex *) input_items[0];
      float *out = (float *) output_items[0];
      //char *out_2 = (char *) output_items[1]; // for debugging
      // float *out_2 = (float *) output_items[1];
      //char *out_2 = (char *) output_items[1];

      int written_sync =0;
      int written = 0, consumed = 0;
      int RN16_index , EPC_index;

      std::vector<float> RN16_samples_real;
      std::vector<float> EPC_samples_real;

      std::vector<gr_complex> RN16_samples_complex;
      std::vector<gr_complex> EPC_samples_complex;

      std::vector<float> RN16_bits;
      int number_of_half_bits = 0;

      std::vector<float> EPC_bits;

      int RN16_preamble_bits = 4; // 1010
      int RN16_preamble [] = {1,0,1,0};

      if (reader_state->decoder_status == DECODER_DECODE_RN16 && ninput_items[0] >= reader_state->n_samples_to_ungate)
      {
        //RN16_index = tag_sync(in,ninput_items[0]);
        RN16_index = 0;
        

        // RN16 bits are passed to the next block for the creation of ACK message
        if ((RN16_index >= 0) && (RN16_index + (n_samples_TAG_BIT)*(RN16_BITS-1) <= ninput_items[0]))
        {
          int recv_rn16[4];
          std::cout << "Preamble : ";
          int offset = find_offset(in);
          //GR_LOG_INFO(d_logger, "Max offset is: " + std::to_string(offset));

          float average_ampl = avg_fm0(in, offset);
          // GR_LOG_INFO(d_logger, "Average ampl of fm0: " + std::to_string(average_ampl));

          for (float j = RN16_index+offset; j < ninput_items[0]; j += n_samples_TAG_BIT )
          {
            number_of_half_bits+=2;
            int k = round(j);
            // GR_LOG_INFO(d_logger, "Current k is: " + std::to_string(k));
            // GR_LOG_INFO(d_logger, std::abs(in[k]))
            float first_half = 0;
            for (int l = 1; l < n_samples_TAG_BIT/2; l ++){
              first_half += std::abs(in[k+l]) - average_ampl;
            }
            first_half = first_half / 4;
            
            k = round(j + n_samples_TAG_BIT/2);
            float sec_half = 0;
            for (int l = 1; l < n_samples_TAG_BIT/2; l ++){
              sec_half += std::abs(in[k+l]) - average_ampl;
            }
            sec_half = sec_half / 4;

            int curr_reading = -1;
            if (((first_half * sec_half) < 0 )){
              //out[written] = 0;  
              std::cout << "0"; 
              recv_rn16[written] = 0;
            }
            else
            { 
              //out[written] = 1; 
              std::cout << "1"; 
              recv_rn16[written] = 1;
            }
            written ++;
            if (number_of_half_bits == 2*RN16_preamble_bits)
            {            
              std::cout << std::endl;
              break;
            }
          }
          if (std::equal(std::begin(recv_rn16), std::end(recv_rn16), std::begin(RN16_preamble)))
          {
            GR_LOG_INFO(d_logger, "Tag");
            out[0] = 1;
          }
          // else{
          //   out[0] = 0;
          // }
          produce(0,1);
          reader_state->gen2_logic_status = IDLE;
        }      
        else
        {
          reader_state->reader_stats.cur_slot_number++;
          if(reader_state->reader_stats.cur_slot_number > reader_state->reader_stats.max_slot_number)
          {
            reader_state->reader_stats.cur_slot_number = 1;
            reader_state->reader_stats.unique_tags_round.push_back(reader_state->reader_stats.tag_reads.size());

            reader_state->reader_stats.cur_inventory_round += 1;

            //if (P_DOWN == true)
            //  reader_state->gen2_logic_status = POWER_DOWN;
            //else
              reader_state->gen2_logic_status = SEND_QUERY;
          }
          else
          {
            reader_state->gen2_logic_status = SEND_QUERY_REP;
          }
        }
        consumed = reader_state->n_samples_to_ungate;
      }
      consume_each(consumed);
      return WORK_CALLED_PRODUCE;
    }


    /* Function adapted from https://www.cgran.org/wiki/Gen2 */
    int tag_decoder_impl::check_crc(char * bits, int num_bits)
    {
      register unsigned short i, j;
      register unsigned short crc_16, rcvd_crc;
      unsigned char * data;
      int num_bytes = num_bits / 8;
      data = (unsigned char* )malloc(num_bytes );
      int mask;

      for(i = 0; i < num_bytes; i++)
      {
        mask = 0x80;
        data[i] = 0;
        for(j = 0; j < 8; j++)
        {
          if (bits[(i * 8) + j] == '1'){
          data[i] = data[i] | mask;
        }
        mask = mask >> 1;
        }
      }
      rcvd_crc = (data[num_bytes - 2] << 8) + data[num_bytes -1];

      crc_16 = 0xFFFF;
      for (i=0; i < num_bytes - 2; i++)
      {
        crc_16^=data[i] << 8;
        for (j=0;j<8;j++)
        {
          if (crc_16&0x8000)
          {
            crc_16 <<= 1;
            crc_16 ^= 0x1021;
          }
          else
            crc_16 <<= 1;
        }
      }
      crc_16 = ~crc_16;

      if(rcvd_crc != crc_16)
        return -1;
      else
        return 1;
    }
  } /* namespace rfid */
} /* namespace gr */
