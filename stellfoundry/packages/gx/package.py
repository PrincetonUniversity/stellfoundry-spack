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


class Gx(MakefilePackage):
    """GX, a GPU-native gyrokinetic turbulence code for tokamak and stellarator design. """

    # Package info
    homepage = "https://bitbucket.org/gyrokinetics/gx/src/gx/"
    git = "https://bitbucket.org/gyrokinetics/gx.git"
    maintainers("github_user1", "github_user2")

    version("develop", branch="gx")

    # FIXME: Add dependencies if required.
    depends_on("nccl+cuda cuda_arch=80")
    depends_on("gsl")
    depends_on("netcdf-c")

    def setup_build_environment(self, env):
        print("gsl:", self.spec["gsl"].prefix)
        print("nccl:", self.spec["nccl"].prefix)
        #print("netcdf-c:", self.spec["netcdf-c"].prefix)
        env.set("GK_SYSTEM", "perlmutter")
        #env.set("NETCDF_DIR", self.spec["netcdf-c"].prefix)
        env.set("GSL_ROOT", self.spec["gsl"].prefix)
        env.set("LD_LIBRARY_PATH", f'{self.spec["gsl"].prefix}/lib:' + os.getenv("LD_LIBRARY_PATH", ""))

    def edit(self, spec, prefix):
        makefile = FileFilter(os.path.join("Makefiles", "Makefile.perlmutter"))
        makefile.filter(r"-lnetcdff",  "") 

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        install_tree(".", prefix)

