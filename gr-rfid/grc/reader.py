#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: EE4002D
# GNU Radio version: v3.8.5.0-6-g57bd109d

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio import zeromq
import rfid


class reader(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "EE4002D")

        ##################################################
        # Variables
        ##################################################
        self.zmq_addr = zmq_addr = "tcp://*:5558"
        self.tx_gain = tx_gain = 70
        self.tx_bw = tx_bw = 1e6
        self.rx_gain = rx_gain = 30
        self.rx_bw = rx_bw = 1e6
        self.path_to_data = path_to_data = "/home/sakeru/Desktop/fyp/Gen2-UHF-RFID-Reader/gr-rfid/misc/data/"
        self.num_taps = num_taps = [1] * 25
        self.freq = freq = 900e6
        self.decim = decim = 4
        self.dac_rate = dac_rate = 1e6
        self.ampl = ampl = 1
        self.adc_rate = adc_rate = 2e6

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_char, 1, zmq_addr, 100, False, -1)
        self.uhd_usrp_source_1 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_1.set_center_freq(freq, 0)
        self.uhd_usrp_source_1.set_gain(rx_gain, 0)
        self.uhd_usrp_source_1.set_antenna('RX2', 0)
        self.uhd_usrp_source_1.set_bandwidth(rx_bw, 0)
        self.uhd_usrp_source_1.set_samp_rate(adc_rate)
        self.uhd_usrp_source_1.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.uhd_usrp_sink_2 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_2.set_center_freq(freq+200e3, 0)
        self.uhd_usrp_sink_2.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_2.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_2.set_samp_rate(dac_rate)
        self.uhd_usrp_sink_2.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.rfid_tag_decoder_0 = rfid.tag_decoder(int(adc_rate/decim))
        self.rfid_reader_0 = rfid.reader(int(adc_rate/decim), int(dac_rate))
        self.rfid_gate_0 = rfid.gate(int(adc_rate/decim))
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decim,
                taps=None,
                fractional_bw=0.4)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(ampl)
        self.blocks_float_to_uchar_0 = blocks.float_to_uchar()
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_sink_6 = blocks.file_sink(gr.sizeof_gr_complex*1, path_to_data+"to_complex", False)
        self.blocks_file_sink_6.set_unbuffered(False)
        self.blocks_file_sink_4 = blocks.file_sink(gr.sizeof_float*1, path_to_data+"reader", False)
        self.blocks_file_sink_4.set_unbuffered(False)
        self.blocks_file_sink_3 = blocks.file_sink(gr.sizeof_gr_complex*1, path_to_data+"gate", False)
        self.blocks_file_sink_3.set_unbuffered(True)
        self.blocks_file_sink_2 = blocks.file_sink(gr.sizeof_gr_complex*1, path_to_data+"matched_filter", False)
        self.blocks_file_sink_2.set_unbuffered(True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, path_to_data+"source", False)
        self.blocks_file_sink_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_file_sink_6, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.uhd_usrp_sink_2, 0))
        self.connect((self.blocks_float_to_uchar_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_file_sink_2, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.rfid_gate_0, 0))
        self.connect((self.rfid_gate_0, 0), (self.blocks_file_sink_3, 0))
        self.connect((self.rfid_gate_0, 0), (self.rfid_tag_decoder_0, 0))
        self.connect((self.rfid_reader_0, 0), (self.blocks_file_sink_4, 0))
        self.connect((self.rfid_reader_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.rfid_tag_decoder_0, 0), (self.blocks_float_to_uchar_0, 0))
        self.connect((self.rfid_tag_decoder_0, 0), (self.rfid_reader_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.rational_resampler_xxx_0, 0))


    def get_zmq_addr(self):
        return self.zmq_addr

    def set_zmq_addr(self, zmq_addr):
        self.zmq_addr = zmq_addr

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_2.set_gain(self.tx_gain, 0)

    def get_tx_bw(self):
        return self.tx_bw

    def set_tx_bw(self, tx_bw):
        self.tx_bw = tx_bw

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_1.set_gain(self.rx_gain, 0)

    def get_rx_bw(self):
        return self.rx_bw

    def set_rx_bw(self, rx_bw):
        self.rx_bw = rx_bw
        self.uhd_usrp_source_1.set_bandwidth(self.rx_bw, 0)

    def get_path_to_data(self):
        return self.path_to_data

    def set_path_to_data(self, path_to_data):
        self.path_to_data = path_to_data
        self.blocks_file_sink_0.open(self.path_to_data+"source")
        self.blocks_file_sink_2.open(self.path_to_data+"matched_filter")
        self.blocks_file_sink_3.open(self.path_to_data+"gate")
        self.blocks_file_sink_4.open(self.path_to_data+"reader")
        self.blocks_file_sink_6.open(self.path_to_data+"to_complex")

    def get_num_taps(self):
        return self.num_taps

    def set_num_taps(self, num_taps):
        self.num_taps = num_taps

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_2.set_center_freq(self.freq+200e3, 0)
        self.uhd_usrp_source_1.set_center_freq(self.freq, 0)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim

    def get_dac_rate(self):
        return self.dac_rate

    def set_dac_rate(self, dac_rate):
        self.dac_rate = dac_rate
        self.uhd_usrp_sink_2.set_samp_rate(self.dac_rate)

    def get_ampl(self):
        return self.ampl

    def set_ampl(self, ampl):
        self.ampl = ampl
        self.blocks_multiply_const_vxx_0.set_k(self.ampl)

    def get_adc_rate(self):
        return self.adc_rate

    def set_adc_rate(self, adc_rate):
        self.adc_rate = adc_rate
        self.uhd_usrp_source_1.set_samp_rate(self.adc_rate)





def main(top_block_cls=reader, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
