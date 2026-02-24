# Copyright (c) 2018 Mathieu Duponchelle <mathieu@centricular.com>
#
# This file is part of the FFmpeg Meson build
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, see <http://www.gnu.org/licenses/>.

import itertools
import re
import os
from pathlib import Path
import io
from collections import defaultdict

ASM_EXTS = ['asm', 'S', 'c']

SOURCE_TYPE_EXTS_MAP = {
    'c': ['c', 'cpp', 'm', 'cl', 'S'],
    'h': ['h'],
    'asm': ASM_EXTS,
    'armv5te': ASM_EXTS,
    'armv6': ASM_EXTS,
    'armv8': ASM_EXTS,
    'vfp': ASM_EXTS,
    'neon': ASM_EXTS,
    'test-prog': ['c'],
    'mmx': ['c'],
    'shlib': ['c'],
    'slib': ['c'],
    'cuda': ['cu'],
}
SOURCE_TYPE_DOUBLE_EXTS_MAP = {
    'metallib.o': ['metal'],
    'ptx.o': ['cu']
}
SOURCE_TYPE_DIRS = {'test-prog': 'tests'}


def add_source(f, source: str, prefix='', suffix=''):
    if not source.startswith(('opencl/', 'metal/', 'cuda/', '../', 'h26x/', 'hevc/')):
        source = source.split('/', maxsplit=1)[-1]
    f.write("%s'%s'%s" % (prefix, source, suffix))


def add_language(languages_map, ext, label):
    if ext == 'cpp':
        languages_map[label].add('cpp')
    elif ext == 'm':
        languages_map[label].add('objc')


def make_to_meson(path):
    source_maps = {
      'c': defaultdict(list),
      'asm': defaultdict(list),
      'armv5te': defaultdict(list),
      'armv6': defaultdict(list),
      'armv8': defaultdict(list),
      'vfp': defaultdict(list),
      'neon': defaultdict(list),
      'test-prog': defaultdict(list),
      'mmx': defaultdict(list),
      'shlib': defaultdict(list),
      'slib': defaultdict(list),
    }

    skipped = set()

    with open(os.path.join(path, 'Makefile'), 'r') as f:
        accum = []
        accumulate = False
        optional = False
        source_type = None
        languages_map = defaultdict(set)

        for l in f.readlines():
            l = l.strip()
            l = l.rsplit('#', 1)[0]

            if accumulate:
                ofiles = l
            elif m := re.match(r'OBJS-\$\((?P<neg>!?)(?:CONFIG|HAVE)_(?P<label>[^\)]+)\)\s*\+=\s*(?P<files>.+)', l):
                label = m.group('label')
                if m.group('neg'):
                    label = '!' + label
                ofiles = m.group('files')
                source_type = 'c'  # arguable ^^
            elif re.match(r'OBJS-.*HAVE.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('HAVE_')[1].rstrip(' )')
                source_type = 'c'
            elif re.match(r'OBJS-(ffmpeg|ffplay)\s+\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('OBJS-')[1]
                source_type = 'c' # arguable ^^
            elif re.match(r'DNN-OBJS-.*CONFIG.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('CONFIG_')[1].rstrip(' )')
                source_type = 'c'  # arguable too ^^
            elif re.match('HEADERS.*=.*', l):
                label = 'headers'
                ofiles = l.split('=')[1]
                source_type = 'h'
            elif re.match('OBJS.*=.*', l):
                label = ''
                ofiles = l.split('=')[1]
                source_type = 'c'
            elif re.match(r'X86ASM-OBJS-.*CONFIG.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('CONFIG_')[1].rstrip(' )')
                source_type = 'asm'
            elif re.match('X86ASM-OBJS.*=.*', l):
                label = ''
                ofiles = l.split('=')[1]
                source_type = 'asm'
            elif re.match(r'STLIBOBJS-.*CONFIG.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('CONFIG_')[1].rstrip(' )')
                source_type = 'slib'
            elif re.match(r'SHLIBOBJS-.*CONFIG.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('CONFIG_')[1].rstrip(' )')
                source_type = 'shlib'
            elif re.match('STLIBOBJS.*=.*', l):
                label = ''
                ofiles = l.split('=')[1]
                source_type = 'slib'
            elif re.match('SHLIBOBJS.*=.*', l):
                label = ''
                ofiles = l.split('=')[1]
                source_type = 'shlib'
            elif re.match(r'TLS-OBJS-.*CONFIG.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('CONFIG_')[1].rstrip(' )')
                source_type = 'c'  # arguable ^^
            elif re.match(r'MMX-OBJS-.*CONFIG.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('CONFIG_')[1].rstrip(' )')
                source_type = 'mmx'
            elif re.match(r'MMX-OBJS-.*HAVE.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('HAVE_')[1].rstrip(' )')
                source_type = 'mmx'
            elif re.match('MMX-OBJS.*=.*', l):
                label = ''
                ofiles = l.split('=')[1]
                source_type = 'mmx'
            elif re.match(r'ARMV5TE-OBJS-.*CONFIG.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('CONFIG_')[1].rstrip(' )')
                source_type = 'armv5te'
            elif re.match(r'ARMV5TE-OBJS-.*HAVE.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('HAVE_')[1].rstrip(' )')
                source_type = 'armv5te'
            elif re.match('ARMV5TE-OBJS.*=.*', l):
                label = ''
                ofiles = l.split('=')[1]
                source_type = 'armv5te'
            elif re.match(r'ARMV6-OBJS-.*CONFIG.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('CONFIG_')[1].rstrip(' )')
                source_type = 'armv6'
            elif re.match(r'ARMV6-OBJS-.*HAVE.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('HAVE_')[1].rstrip(' )')
                source_type = 'armv6'
            elif re.match('ARMV6-OBJS.*=.*', l):
                label = ''
                ofiles = l.split('=')[1]
                source_type = 'armv6'
            elif re.match(r'ARMV8-OBJS-.*CONFIG.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('CONFIG_')[1].rstrip(' )')
                source_type = 'armv8'
            elif re.match(r'ARMV8-OBJS-.*HAVE.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('HAVE_')[1].rstrip(' )')
                source_type = 'armv8'
            elif re.match('ARMV8-OBJS.*=.*', l):
                label = ''
                ofiles = l.split('=')[1]
                source_type = 'armv8'
            elif re.match(r'VFP-OBJS-.*CONFIG.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('CONFIG_')[1].rstrip(' )')
                source_type = 'vfp'
            elif re.match(r'VFP-OBJS-.*HAVE.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('HAVE_')[1].rstrip(' )')
                source_type = 'vfp'
            elif re.match('VFP-OBJS.*=.*', l):
                label = ''
                ofiles = l.split('=')[1]
                source_type = 'vfp'
            elif re.match(r'NEON-OBJS-.*CONFIG.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('CONFIG_')[1].rstrip(' )')
                source_type = 'neon'
            elif re.match(r'NEON-OBJS-.*HAVE.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('HAVE_')[1].rstrip(' )')
                source_type = 'neon'
            elif re.match('NEON-OBJS.*=.*', l):
                label = ''
                ofiles = l.split('=')[1]
                source_type = 'neon'
            elif re.match(r'TESTPROGS-.*CONFIG.*\+\=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('CONFIG_')[1].rstrip(' )')
                source_type = 'test-prog'
            elif re.match(r'TESTPROGS-.*HAVE.*\+=.*', l):
                label, ofiles = l.split('+=')
                label = label.split('HAVE_')[1].rstrip(' )')
                source_type = 'test-prog'
            elif re.match('TESTOBJS.*=', l):
                label = ''
                ofiles = l.split('=')[1]
                source_type = 'c'
            elif re.match('TESTPROGS.*=', l):
                label = ''
                ofiles = l.split('=')[1]
                source_type = "test-prog"
            else:
                continue

            accumulate = ofiles.endswith('\\')
            ofiles = ofiles.strip('\\')
            ofiles = ofiles.split()
            ifiles = []
            for ofile in ofiles:
                basename = ofile.split('.')
                if len(basename) > 2:
                    exts = SOURCE_TYPE_DOUBLE_EXTS_MAP.get('.'.join(basename[1:]), [])
                else:
                    exts = SOURCE_TYPE_EXTS_MAP[source_type]
                fname = basename[0]
                for ext in exts:
                    tmpf = fname + '.' + ext
                    root = path.split('/')[0]
                    path_options = [
                        os.path.join(path, SOURCE_TYPE_DIRS.get(source_type, ''), tmpf),
                        os.path.join(path, SOURCE_TYPE_DIRS.get(source_type, ''), os.path.basename(tmpf)),
                        # x86/h26x
                        os.path.join(root, SOURCE_TYPE_DIRS.get(source_type, ''), os.path.dirname(tmpf), os.path.basename(tmpf))
                    ]
                    for i, p in enumerate(path_options):
                        if os.path.exists(p):
                            # What path needs to go into the Meson file?
                            src_path = Path(p)
                            meson_path = Path(path)
                            if i == 2:
                                if src_path.is_relative_to(meson_path):
                                    tmpf = src_path.relative_to(meson_path).as_posix()
                                else:
                                    src_path = src_path.absolute()
                                    meson_path = meson_path.absolute().parent
                                    tmpf = '../' + src_path.relative_to(meson_path).as_posix()
                            elif i == 1:
                                tmpf = src_path.relative_to(meson_path).as_posix()
                            ifiles.append(tmpf)
                            add_language(languages_map, ext, label)
                            break
                    # print("WARNING: %s do not exist" % str(path_options))

            if len([of for of in ofiles if not of.startswith("$")]) != len(ifiles):
                print("WARNING: %s and %s size don't match, not building!" % ([of for of in ofiles if not of.startswith("$")], ifiles))
                skipped.add(label)

            if accumulate:
                accum += ifiles
            else:
                map_ = source_maps.get(source_type, source_maps['c'])
                map_[label] += accum + ifiles
                accum = []

        # Makefiles can end with '\' and this is just a porting script ;)
        if accum:
            map_ = source_maps.get(source_type, source_maps['c'])
            map_[label] += accum
            accum = []


    lines = []
    has_not_generated = False
    try:
        with open(os.path.join(path, 'meson.build'), 'r') as meson_file:
            for l in meson_file.readlines():
                if l == '#### --- GENERATED --- ####\n':
                    lines += [l, '\n']
                    has_not_generated = True
                    break
                lines.append(l)
    except FileNotFoundError:
        pass

    f = io.StringIO()

    c_source_maps = defaultdict(list)
    cuda_source_maps = defaultdict(list)
    for k, v in source_maps['c'].items():
        def is_cu(f):
            return f.endswith('.cu')
        for k2, v2 in itertools.groupby(sorted(v, key=is_cu), is_cu):
            if k2:
                cuda_source_maps[k].extend(list(v2))
            else:
                c_source_maps[k].extend(list(v2))

    source_types = (
        ('', c_source_maps),
        ('x86asm_', source_maps['asm']),
        ('armv5te_', source_maps['armv5te']),
        ('armv6_', source_maps['armv6']),
        ('armv8_', source_maps['armv8']),
        ('neon_', source_maps['neon']),
        ('vfp_', source_maps['vfp']),
        ('mmx_', source_maps['mmx']),
        ('shlib_', source_maps['shlib']),
        ('slib_', source_maps['slib']),
        ('cuda_', cuda_source_maps),
    )

    for source_type, map_ in source_types:
        if all(len(fs) == 0 for fs in map_.values()):
            continue

        default_sources = map_.pop('', [])

        if default_sources:
            f.write('%ssources = files(\n' % '_'.join((path.replace('/', '_'), source_type)))
            for source in default_sources:
                if '$' in source:
                    print ('Warning: skipping %s' % source)
                    continue
                add_source(f, source, prefix='  ', suffix=',\n')
            f.write(')\n\n')

        default_sources = map_.pop('headers', [])

        if default_sources:
            f.write('%sheaders = files(\n' % '_'.join((path.replace('/', '_'), source_type)))
            for source in default_sources:
                if '$' in source:
                    print ('Warning: skipping %s' % source)
                    continue
                add_source(f, source, prefix='  ', suffix=',\n')
            f.write(')\n\n')

        if len(map_) == 0:
            continue  # No more entries to fill

        f.write('%soptional_sources = {\n' % '_'.join((path.replace('/', '_'), source_type)))
        for label in sorted (map_):
            l = len (map_[label])
            if l == 0:
                continue
            if label in skipped:
                f.write("  # '%s' : files(" % label.lower())
            else:
                f.write("  '%s' : files(" % label.lower())
            for i, source in enumerate(map_[label]):
                if '$' in source:
                    print ('Warning: skipping %s' % source)
                    continue
                add_source(f, source)
                if i + 1 < l:
                    f.write(',')
            f.write('),\n')
        f.write('}\n\n')

    test_source_map = source_maps['test-prog']

    default_test_sources = test_source_map.pop('', [])

    if default_test_sources:
        f.write('%s_tests = [\n' % path.replace('/', '_'))
        for source in default_test_sources:
            if '$' in source:
                print ('Warning: skipping %s' % source)
                continue
            basename = os.path.basename(source)
            testname = os.path.splitext(basename)[0]
            f.write("  ['%s', files('tests/%s')],\n" % (testname, basename))
        f.write(']\n\n')

    if test_source_map:
        f.write('%s_optional_tests = {\n' % path.replace('/', '_'))
        for label in sorted (test_source_map):
            test_sources = test_source_map[label]
            if len(test_sources) == 0:
                continue
            f.write("  '%s' : [\n" % label.lower())
            for source in test_sources:
                if '$' in source:
                    print ('Warning: skipping %s' % source)
                    continue
                basename = os.path.basename(source)
                testname = os.path.splitext(basename)[0]
                f.write("    ['%s', files('tests/%s')],\n" % (testname, basename))
            f.write('  ],\n')
        f.write('}\n\n')

    if languages_map:
        f.write('languages_map += {\n')
        for label, languages in languages_map.items():
            f.write("  '%s': %s,\n" % (label.lower(), list(languages)))
        f.write('}\n')

    if has_not_generated:
        lines.append(f.getvalue())
        with open(os.path.join(path, 'meson.build'), 'r') as meson_file:
            out_generated = False
            for l in meson_file.readlines():
                if l == '#### --- END GENERATED --- ####\n':
                    out_generated = True
                if out_generated:
                    lines.append(l)
        content = ''.join(lines)
    else:
        content = f.getvalue()


    with open(os.path.join(path, 'meson.build'), 'w') as meson_file:
        meson_file.write(content)

paths = [
        'fftools',
        'libavdevice',
        'libavformat',
        'libavutil',
        'libavutil/aarch64',
        'libavutil/arm',
        'libavutil/x86',
        'libswscale',
        'libswscale/aarch64',
        'libswscale/arm',
        'libswscale/x86',
        'libavcodec',
        'libavcodec/bsf',
        'libavcodec/aac',
        'libavcodec/aarch64',
        'libavcodec/aarch64/vvc',
        'libavcodec/arm',
        'libavcodec/bsf',
        'libavcodec/hevc',
        # 'libavcodec/h26x',
        'libavcodec/neon',
        'libavcodec/opus',
        'libavcodec/x86',
        'libavcodec/x86/vvc',
        'libavcodec/vvc',
        'libswresample',
        'libswresample/aarch64',
        'libswresample/arm',
        'libswresample/x86',
        'libavfilter',
        'libavfilter/aarch64',
        'libavfilter/x86',
        'libavfilter/dnn',
        'libpostproc',
]

if __name__=='__main__':
    for path in paths:
        make_to_meson(path)
