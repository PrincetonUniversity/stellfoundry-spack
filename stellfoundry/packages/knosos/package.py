# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install stellopt
#
# You can edit this file again by typing:
#
#     spack edit stellopt
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *
import os
import subprocess


class Knosos(MakefilePackage):
    """ The KiNetic Orbit-averaging SOlver for Stellarators (KNOSOS) """

    # Package info
    homepage = "https://github.com/joseluisvelasco/KNOSOS.git"
    git = "https://github.com/joseluisvelasco/KNOSOS.git"
    maintainers("github_user1", "github_user2")

    version("develop", branch="master")

    # FIXME: Add dependencies if required.
    depends_on("petsc@3.11")
    depends_on("netcdf-fortran")
    # depends_on("netcdf-fortran^netcdf-c+mpi")

    build_directory = "SOURCES"

    def setup_build_environment(self, env):
        print("netcdf-c:", self.spec["netcdf-c"].prefix)
        print("netcdf-fortran:", self.spec["netcdf-fortran"].prefix)
        print("petsc:", self.spec["petsc"].prefix)
        env.set("NETCDF_DIR", self.spec["netcdf-c"].prefix)
        env.set("NETCDF_F_DIR", self.spec["netcdf-fortran"].prefix)
        env.set("PETSC_DIR", self.spec["petsc"].prefix)

    def edit(self, spec, prefix):
        with working_dir('SOURCES'):
            with open('Makefile', 'r') as mf:
                lines = mf.readlines()
            
            is_the_block = False
            for i, line in enumerate(lines):
                if 'ifeq ($(CASE), perlmutter)' in line:
                    is_the_block = True
                if is_the_block and line.startswith("endif"):
                    lines.insert(i, "LFLAGS   += -L${NETCDF_F_DIR}/lib -lnetcdff\n")
                    lines.insert(i, "IFLAGS   += -I${NETCDF_F_DIR}/include\n")
                    lines.insert(i, "IFLAGS   += -I.\n")
                    break
            
            with open('Makefile', 'w') as mf:
                mf.writelines(lines)

    def build(self, spec, prefix):
        with working_dir('SOURCES'):
            make(parallel=False)

    def install(self, spec, prefix):
        with working_dir('SOURCES'):
            mkdirp(prefix.bin)
            install("knosos.x", prefix.bin)

