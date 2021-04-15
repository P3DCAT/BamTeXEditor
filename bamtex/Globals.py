from panda3d.core import LVecBase4f
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox
from . import OptionGlobals
from .Option import Option

TextureType = 0
TextureFormat = 1
UsageHint = 2
WrapMode = 3
FilterType = 4
CompressionMode = 5
QualityLevel = 6
AutoTextureScale = 7

Enums = [
    [
        '1D Texture',
        '2D Texture',
        '3D Texture',
        '2D Texture Array',
        'Cube Map',
        'Buffer Texture',
        'Cube Map Array',
        '1D Texture Array'
    ],
    [
        'Unknown',
        'Depth Stencil',
        'Color Index',
        'Red',
        'Green',
        'Blue',
        'Alpha',
        'RGB',
        'RGB 5-bit',
        'RGB 8-bit',
        'RGB 12-bit',
        'RGB 332',
        'RGBA',
        'RGBM',
        'RGBA 4-bit',
        'RGBA 5-bit',
        'RGBA 8-bit',
        'RGBA 12-bit',
        'Luminance',
        'Luminance Alpha',
        'Luminance Alpha Mask',
        'RGBA 16-bit',
        'RGBA 32-bit',
        'Depth Component',
        'Depth Component 16-bit',
        'Depth Component 24-bit',
        'Depth Component 32-bit',
        'R 16-bit',
        'RG 16-bit',
        'RGB 16-bit',
        'SRGB',
        'SRGB Alpha',
        'S Luminance',
        'S Luminance Alpha',
        'R32I',
        'R 32-bit',
        'RG 32-bit',
        'RGB 32-bit',
        'R8I',
        'RG8I',
        'RGB8I',
        'RGBA8I',
        'R11/G11/B10',
        'RGB9 E5',
        'RGB10 A2',
        'RG',
        'R16I'
    ],
    [
        'Client',
        'Stream',
        'Dynamic',
        'Static',
        'Unspecified'
    ],
    [
        'Unspecified',
        'Clamp',
        'Repeat',
        'Mirror',
        'Mirror Once',
        'Border Color'
    ],
    [
        'Unspecified',
        'Nearest',
        'Linear',
        'Mipmap Point',
        'Mipmap Linear',
        'Mipmap Bilinear',
        'Mipmap Trilinear'
    ],
    [
        'Default',
        'Off',
        'On',
        'FXT1',
        'DXT1',
        'DXT2',
        'DXT3',
        'DXT4',
        'DXT5'
    ],
    [
        'Unspecified',
        'Default',
        'Fastest',
        'Normal',
        'Best'
    ],
    [
        'None',
        'Down',
        'Up',
        'Pad',
        'Unspecified'
    ]
]

TextureFields = [
    ['General', [
        Option('name', 'Texture name', OptionGlobals.STRING),
        Option('filename', 'Color filename', OptionGlobals.STRING),
        Option('alpha_filename', 'Alpha filename', OptionGlobals.STRING),
        Option('primary_file_num_channels', 'Color channels', OptionGlobals.UINT8, bam_version=(4, 2)),
        Option('alpha_file_channel', 'Alpha file channel', OptionGlobals.UINT8, bam_version=(4, 3)),
        Option('texture_type', 'Texture type', OptionGlobals.ENUM, enum_type=TextureType),
        Option('tex_format', 'Texture format', OptionGlobals.ENUM, enum_type=TextureFormat),
        Option('num_components', 'Number of components', OptionGlobals.UINT8),
        Option('has_rawdata', 'Raw data available', OptionGlobals.BOOL),
        Option('has_read_mipmaps', 'Mipmaps read', OptionGlobals.BOOL, bam_version=(6, 32))
    ]],
    ['Texture UV', [
        Option('wrap_u', 'Wrap U', OptionGlobals.ENUM, enum_type=WrapMode),
        Option('wrap_v', 'Wrap V', OptionGlobals.ENUM, enum_type=WrapMode),
        Option('wrap_w', 'Wrap W', OptionGlobals.ENUM, enum_type=WrapMode),
        Option('minfilter', 'Minfilter', OptionGlobals.ENUM, enum_type=FilterType),
        Option('magfilter', 'Magfilter', OptionGlobals.ENUM, enum_type=FilterType),
        Option('anisotropic_degree', 'Anisotropic degree', OptionGlobals.INT16),
        Option('border_color', 'Border color', OptionGlobals.COLOR)
    ]],
    ['LOD', [
        Option('min_lod', 'Min LOD', OptionGlobals.FLOAT, bam_version=(6, 36)),
        Option('max_lod', 'Max LOD', OptionGlobals.FLOAT, bam_version=(6, 36)),
        Option('lod_bias', 'LOD bias', OptionGlobals.FLOAT, bam_version=(6, 36))
    ]],
    ['Miscellaneous', [
        Option('compression', 'Compression', OptionGlobals.ENUM, enum_type=CompressionMode, bam_version=(6, 1)),
        Option('quality_level', 'Quality level', OptionGlobals.ENUM, enum_type=QualityLevel, bam_version=(6, 16)),
        Option('usage_hint', 'Usage hint', OptionGlobals.ENUM, enum_type=UsageHint),
        Option('auto_texture_scale', 'Auto texture scale', OptionGlobals.ENUM, enum_type=AutoTextureScale, bam_version=(6, 28)),
        Option('orig_file_x_size', "Original file's X size", OptionGlobals.UINT32),
        Option('orig_file_y_size', "Original file's Y size", OptionGlobals.UINT32)
    ]],
    ['Simple RAM Image', [
        Option('has_simple_ram_image', 'Enabled', OptionGlobals.BOOL),
        Option('simple_x_size', 'X size', OptionGlobals.UINT32),
        Option('simple_y_size', 'Y size', OptionGlobals.UINT32),
        Option('simple_image_date_generated', 'Date generated', OptionGlobals.INT32),
        Option('simple_ram_image', 'Image data', OptionGlobals.BLOB),
        Option('has_clear_color', 'Clear color enabled', OptionGlobals.BOOL),
        Option('clear_color', 'Clear color', OptionGlobals.COLOR)
    ]]
]

def showError(error):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(error)
    msg.setWindowTitle('Error!')
    msg.exec_()

def hexToColor(value):
    value = value.lstrip('#')

    if len(value) != 8:
        return None

    try:
        return QColor(*[int(value[i:i + 2], 16) for i in (2, 4, 6, 0)])
    except:
        return None

def qtColorToPanda(color):
    rgba = [comp / 255.0 for comp in color.getRgb()]
    return LVecBase4f(*rgba)
