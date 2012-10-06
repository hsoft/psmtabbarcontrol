#!/usr/bin/env python

import sys
import os
import os.path as op
import glob
import sysconfig
from waflib import TaskGen
try:
    import hscommon
except ImportError:
    # Probably in the parent folder
    sys.path.insert(0, '..')
from hscommon.build import OSXFrameworkStructure

# Make sure to set CFLAGS and LDFLAGS (to have correct archs and isysroot) first.

top = '.'
out = 'build'

def options(opt):
    opt.load('compiler_c')

def configure(conf):
    conf.env.CC = 'clang'
    conf.load('compiler_c')
    conf.env.FRAMEWORK_COCOA = 'Cocoa'
    # Have the save compile/link flags as our python installation.
    conf.env.append_value('CFLAGS', sysconfig.get_config_var('CFLAGS'))
    conf.env.append_value('LDFLAGS', sysconfig.get_config_var('LDFLAGS'))
    conf.env.append_value('LINKFLAGS', ['-install_name', '@rpath/PSMTabBarControl.framework/PSMTabBarControl'])

def build(ctx):
    ctx.shlib(
        features      = 'c cshlib',
        target        = ctx.bldnode.make_node('PSMTabBarControl'),
        source        = ctx.srcnode.ant_glob('*.m'),
        includes      = [ctx.srcnode],
        use           = 'COCOA',
    )

def build_framework(ctx):
    fmk = OSXFrameworkStructure('PSMTabBarControl.framework')
    fmk.create('Info.plist')
    fmk.copy_executable('build/PSMTabBarControl')
    fmk.copy_headers(*glob.glob('*.h'))
    fmk.copy_resources(*glob.glob('images/*.*'))
    fmk.create_symlinks()

@TaskGen.extension('.m')
def m_hook(self, node):
    return self.create_compiled_task('c', node)

