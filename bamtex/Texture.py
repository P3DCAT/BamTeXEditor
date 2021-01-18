from p3bamboo.BamObject import BamObject
from p3bamboo.BamGlobals import read_vec4, write_vec

"""
  P3BAMBOO
  Panda3D BAM file library

  Author: Disyer
  Date: 2020/10/16
"""
class Texture(BamObject):

    def __init__(self, bam_file, bam_version):
        BamObject.__init__(self, bam_file, bam_version)

    def load(self, di):
        BamObject.load(self, di)

        self.name = di.get_string()
        self.filename = di.get_string()
        self.alpha_filename = di.get_string()

        if self.bam_version >= (4, 2):
            self.primary_file_num_channels = di.get_uint8()
        else:
            self.primary_file_num_channels = 0

        if self.bam_version >= (4, 3):
            self.alpha_file_channel = di.get_uint8()
        else:
            self.alpha_file_channel = 0

        self.has_rawdata = di.get_bool()
        self.texture_type = di.get_uint8() # TextureType

        if self.bam_version >= (6, 32):
            self.has_read_mipmaps = di.get_bool()
        else:
            self.has_read_mipmaps = False

        # Fill in body

        # SamplerState (default_sampler)
        self.wrap_u = di.get_uint8() # WrapMode
        self.wrap_v = di.get_uint8() # WrapMode
        self.wrap_w = di.get_uint8() # WrapMode
        self.minfilter = di.get_uint8() # FilterType
        self.magfilter = di.get_uint8() # FilterType
        self.anisotropic_degree = di.get_int16()
        self.border_color = read_vec4(di)

        if self.bam_version >= (6, 36):
            self.min_lod = self.bam_file.read_stdfloat(di)
            self.max_lod = self.bam_file.read_stdfloat(di)
            self.lod_bias = self.bam_file.read_stdfloat(di)
        else:
            self.min_lod = -1000
            self.max_lod = 1000
            self.lod_bias = 0

        # Rest of body
        if self.bam_version >= (6, 1):
            self.compression = di.get_uint8() # CompressionMode
        else:
            self.compression = 0

        if self.bam_version >= (6, 16):
            self.quality_level = di.get_uint8() # QualityLevel
        else:
            self.quality_level = 0

        self.tex_format = di.get_uint8() # Format
        self.num_components = di.get_uint8()
        self.texture_data = di.extract_bytes(di.get_remaining_size())

    def write(self, write_version, dg):
        BamObject.write(self, write_version, dg)

        dg.add_string(self.name)
        dg.add_string(self.filename)
        dg.add_string(self.alpha_filename)

        if write_version >= (4, 2):
            dg.add_uint8(self.primary_file_num_channels)

        if write_version >= (4, 3):
            dg.add_uint8(self.alpha_file_channel)

        dg.add_bool(self.has_rawdata)
        dg.add_uint8(self.texture_type)

        if write_version >= (6, 32):
            dg.add_bool(self.has_read_mipmaps)

        # Fill in body

        # SamplerState (default_sampler)
        dg.add_uint8(self.wrap_u) # WrapMode
        dg.add_uint8(self.wrap_v) # WrapMode
        dg.add_uint8(self.wrap_w) # WrapMode
        dg.add_uint8(self.minfilter) # FilterType
        dg.add_uint8(self.magfilter) # FilterType
        dg.add_int16(self.anisotropic_degree)
        write_vec(dg, self.border_color)

        if write_version >= (6, 36):
            self.bam_file.write_stdfloat(dg, self.min_lod)
            self.bam_file.write_stdfloat(dg, self.max_lod)
            self.bam_file.write_stdfloat(dg, self.lod_bias)

        # Rest of body
        if write_version >= (6, 1):
            dg.add_uint8(self.compression) # CompressionMode

        if write_version >= (6, 16):
            dg.add_uint8(self.quality_level) # QualityLevel

        dg.add_uint8(self.tex_format) # Format
        dg.add_uint8(self.num_components)

        dg.append_data(self.texture_data)

    def __str__(self):
        return ('Texture(name={0}, filename={1}, alpha_filename={2}, primary_file_num_channels={3}, alpha_file_channel={4}, has_rawdata={5}, texture_type={6}, has_read_mipmaps={7}, ' +
            'wrap_u={8}, wrap_v={9}, wrap_w={10}, minfilter={11}, magfilter={12}, anisotropic_degree={13}, border_color={14}, min_lod={15}, max_lod={16}, lod_bias={17}, ' +
            'compression={18}, quality_level={19}, format={20}, num_components={21}').format(
            self.name, self.filename, self.alpha_filename, self.primary_file_num_channels, self.alpha_file_channel, self.has_rawdata, self.texture_type, self.has_read_mipmaps,
            self.wrap_u, self.wrap_v, self.wrap_w, self.minfilter, self.magfilter, self.anisotropic_degree, self.border_color, self.min_lod, self.max_lod, self.lod_bias,
            self.compression, self.quality_level, self.tex_format, self.num_components
        )
