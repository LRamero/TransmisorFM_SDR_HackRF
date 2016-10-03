#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Fm Transmitter
# Generated: Fri Sep 23 17:36:51 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class FM_Transmitter(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Fm Transmitter")
        _icon_path = "C:\Program Files\GNURadio-3.7\share\icons\hicolor\48x48/apps\gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.volumen = volumen = 1
        self.samp_rate = samp_rate = 42.1e3
        self.frec_m = frec_m = 100
        self.deltaF = deltaF = 5000

        ##################################################
        # Blocks
        ##################################################
        _volumen_sizer = wx.BoxSizer(wx.VERTICAL)
        self._volumen_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_volumen_sizer,
        	value=self.volumen,
        	callback=self.set_volumen,
        	label="volumen",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._volumen_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_volumen_sizer,
        	value=self.volumen,
        	callback=self.set_volumen,
        	minimum=0,
        	maximum=50,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_volumen_sizer)
        _deltaF_sizer = wx.BoxSizer(wx.VERTICAL)
        self._deltaF_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_deltaF_sizer,
        	value=self.deltaF,
        	callback=self.set_deltaF,
        	label='deltaF',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._deltaF_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_deltaF_sizer,
        	value=self.deltaF,
        	callback=self.set_deltaF,
        	minimum=2000,
        	maximum=75000,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_deltaF_sizer)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=88.2e3,
        	fft_size=2048,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1000000,
                decimation=int(samp_rate*2),
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_sink_0.set_sample_rate(1000000)
        self.osmosdr_sink_0.set_center_freq(80e6, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(20, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        _frec_m_sizer = wx.BoxSizer(wx.VERTICAL)
        self._frec_m_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_frec_m_sizer,
        	value=self.frec_m,
        	callback=self.set_frec_m,
        	label='frec_m',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._frec_m_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_frec_m_sizer,
        	value=self.frec_m,
        	callback=self.set_frec_m,
        	minimum=100,
        	maximum=20000,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_frec_m_sizer)
        self.blocks_wavfile_source_0 = blocks.wavfile_source("D:\Descargas\Depeche Mode - Precious (HQ).wav", True)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=int(samp_rate),
        	quad_rate=int(samp_rate*2),
        	tau=75e-6,
        	max_dev=deltaF,
        )
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, volumen)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.analog_wfm_tx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.analog_wfm_tx_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.analog_wfm_tx_0, 0))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))    

    def get_volumen(self):
        return self.volumen

    def set_volumen(self, volumen):
        self.volumen = volumen
        self._volumen_slider.set_value(self.volumen)
        self._volumen_text_box.set_value(self.volumen)
        self.analog_const_source_x_0.set_offset(self.volumen)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_frec_m(self):
        return self.frec_m

    def set_frec_m(self, frec_m):
        self.frec_m = frec_m
        self._frec_m_slider.set_value(self.frec_m)
        self._frec_m_text_box.set_value(self.frec_m)

    def get_deltaF(self):
        return self.deltaF

    def set_deltaF(self, deltaF):
        self.deltaF = deltaF
        self._deltaF_slider.set_value(self.deltaF)
        self._deltaF_text_box.set_value(self.deltaF)


def main(top_block_cls=FM_Transmitter, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
