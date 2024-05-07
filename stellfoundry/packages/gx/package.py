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


class Gx(Package):
    """GX, a GPU-native gyrokinetic turbulence code for tokamak and stellarator design. """

    # Package info
    homepage = "https://bitbucket.org/gyrokinetics/gx/src/gx/"
    git = "https://bitbucket.org/gyrokinetics/gx.git"
    maintainers("github_user1", "github_user2")

    version("develop", branch="gx")

    # FIXME: Add dependencies if required.
    depends_on("netcdf-c +parallel-netcdf")
    depends_on("cuda")
    depends_on("gsl")
    depends_on("nccl@1.18.3-cu12")

    def install(self, spec, prefix):
        os.environ["CC"] = self.compiler.cc
        os.environ["CXX"] = self.compiler.cxx
        os.environ["FC"] = self.compiler.fc
        os.environ["MPICC"] = self.compiler.cc
        os.environ["MPICXX"] = self.compiler.cxx
        os.environ["MPIFC"] = self.compiler.fc
        os.environ["GK_SYSTEM"] = "perlmutter"
        os.environ["NETCDF_DIR"] = self.spec["netcdf-c"].prefix
        os.environ["GSL_ROOT"] = self.spec["gsl"].prefix
        os.environ["LD_LIBRARY_PATH"] = f'{self.spec["gsl"].prefix}/lib:' + os.getenv("LD_LIBRARY_PATH", "")
        print("nccl:", self.spec["nccl"].prefix)
        print("netcdf-c:", self.spec["netcdf-c"].prefix)

        makefile = FileFilter(os.path.join("Makefiles", "Makefile.perlmutter"))
        makefile.filter(r"-lnetcdff",  "")

        #cmd = "make test_make"
        cmd = "make"
        process = subprocess.Popen(cmd, shell=True, env=os.environ, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        print("stdout:", stdout)
        print("stderr:", stderr)
        install_tree(".", prefix)

