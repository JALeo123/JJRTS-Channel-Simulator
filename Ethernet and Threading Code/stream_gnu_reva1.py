#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Wed Apr  8 14:50:49 2020
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt, QtCore
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import limesdr
import sys
from gnuradio import qtgui
import numpy
import math

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.phase = phase = 1
        self.RF_Freq = RF_Freq = 20e6

        ##################################################
        # Look-up Tables for Phase Shift
        ##################################################
        phi = numpy.arange(0, 361, 1)
        pi = math.pi
        cos_lut = []
        sin_lut = []
        cos_lut = numpy.cos(pi*phi/180)
        sin_lut = numpy.sin(pi*phi/180)   

        ##################################################
        # Blocks
        ##################################################
        self._phase_range = Range(0, 361, 1, 1, 200)
        self._phase_win = RangeWidget(self._phase_range, self.set_phase, "phase", "counter_slider", int)
        self.top_grid_layout.addWidget(self._phase_win)
        self.limesdr_source_0 = limesdr.source('0009070602470A0E', 0, '')
        self.limesdr_source_0.set_sample_rate(samp_rate)
        self.limesdr_source_0.set_center_freq(RF_Freq, 0)
        self.limesdr_source_0.set_bandwidth(21e6,0)
        self.limesdr_source_0.set_digital_filter(5e3,0)
        self.limesdr_source_0.set_gain(0,0)
        self.limesdr_source_0.set_antenna(2,0)
        self.limesdr_source_0.calibrate(5e6, 0)

        (self.limesdr_source_0).set_min_output_buffer(4096)
        (self.limesdr_source_0).set_max_output_buffer(4096)
        self.limesdr_sink_0 = limesdr.sink('0009070602470A0E', 0, '', '')
        self.limesdr_sink_0.set_sample_rate(samp_rate)
        self.limesdr_sink_0.set_center_freq(30e6, 0)
        self.limesdr_sink_0.set_bandwidth(31e6,0)
        self.limesdr_sink_0.set_digital_filter(5e3,0)
        self.limesdr_sink_0.set_gain(60,0)
        self.limesdr_sink_0.set_antenna(1,0)
        self.limesdr_sink_0.calibrate(5e6, 0)

        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((sin_lut[phase], ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((-cos_lut[phase], ))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_float_0_0 = blocks.complex_to_float(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_float_0_0, 1), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.limesdr_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.limesdr_source_0, 0), (self.blocks_complex_to_float_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_phase(self):
        return self.phase

    def set_phase(self, phase):
        self.phase = phase
        self.blocks_multiply_const_vxx_0_0.set_k((self.phase, ))
        self.blocks_multiply_const_vxx_0.set_k((self.phase, ))

    def get_RF_Freq(self):
        return self.RF_Freq

    def set_RF_Freq(self, RF_Freq):
        self.RF_Freq = RF_Freq
        self.limesdr_source_0.set_center_freq(self.RF_Freq, 0)


def main(top_block_cls=top_block, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
