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
    depends_on("netcdf-c+parallel-netcdf")
    depends_on("cuda")
    depends_on("gsl")

    def install(self, spec, prefix):
        os.environ["CC"] = self.compiler.cc
        os.environ["CXX"] = self.compiler.cxx
        os.environ["FC"] = self.compiler.fc
        os.environ["MPICC"] = self.compiler.cc
        os.environ["MPICXX"] = self.compiler.cxx
        os.environ["MPIFC"] = self.compiler.fc
        os.environ["GK_SYSTEM"] = "perlmutter"
        os.environ["GSL_ROOT"] = self.spec["gsl"].prefix
        os.environ["LD_LIBRARY_PATH"] = f'{self.spec["gsl"].prefix}/lib:' + os.getenv("LD_LIBRARY_PATH", "")

        # makefile = FileFilter(os.path.join("SHARE", "make_perlmutter.inc"))
        # makefile.filter(r"^\s*NETCDF_DIR\s*=.*",  f"  NETCDF_DIR = {self.spec['netcdf-fortran'].prefix}")
        # makefile.filter(r"^\s*HDF5_DIR\s*=.*",  f"  HDF5_DIR = {self.spec['hdf5'].prefix}")
        # makefile.filter(r"^\s*MYHOME\s*=.*",  f"  MYHOME = {os.getcwd()}")

        cmd = "make"
        subprocess.check_output(cmd, shell=True, env=os.environ, cwd=os.getcwd())
        # install_tree(".", prefix)
