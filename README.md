# VGM2WAV  
A simple way to batch convert with vgmstream.  

By default, dragging and dropping files/folders onto the executable will search for the following file types due to them being the ones I use the most:  
- binka
- wem
- fsb
- awb
- bank
  
To convert other formats, call it from cli with:  
`.\vgm2wav input_files -f {formats}`  
where {formats} are a list of file extensions, separated by spaces.  
  
For example, to convert all .hca and .fwav files:  
`.\vgm2wav input_files -f hca fwav`  
  
  
The full list of supported formats can be found in `formats.py` or on the [vgmstream repo](https://github.com/vgmstream/vgmstream/blob/master/src/formats.c).  
  
## Credits:  
[vgmstream](https://vgmstream.org/)  
[Source](https://github.com/vgmstream/vgmstream)  
[LICENSE](https://github.com/vgmstream/vgmstream?tab=License-1-ov-file)