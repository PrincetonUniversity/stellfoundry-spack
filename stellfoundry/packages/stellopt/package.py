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


class Stellopt(Package):
    """STELLOPT, the state-of-the-art stellarator optimization code"""

    # Package info
    homepage = "https://github.com/PrincetonUniversity/STELLOPT"
    git = "https://github.com/jychoi-hpc/STELLOPT.git"
    maintainers("github_user1", "github_user2")

    version("develop", branch="develop")

    # FIXME: Add dependencies if required.
    depends_on("netcdf-fortran")
    depends_on("hdf5+fortran")

    def install(self, spec, prefix):
        os.environ["CC"] = self.compiler.cc
        os.environ["CXX"] = self.compiler.cxx
        os.environ["FC"] = self.compiler.fc
        os.environ["MPICC"] = self.compiler.cc
        os.environ["MPICXX"] = self.compiler.cxx
        os.environ["MPIFC"] = self.compiler.fc

        os.environ["STELLOPT_PATH"] = os.getcwd()
        os.environ["MACHINE"] = "perlmutter"

        makefile = FileFilter(os.path.join("SHARE", "make_perlmutter.inc"))
        makefile.filter(r"^\s*NETCDF_DIR\s*=.*",  f"  NETCDF_DIR = {self.spec['netcdf-fortran'].prefix}")
        makefile.filter(r"^\s*HDF5_DIR\s*=.*",  f"  HDF5_DIR = {self.spec['hdf5'].prefix}")
        makefile.filter(r"^\s*MYHOME\s*=.*",  f"  MYHOME = {self.spec.prefix}")

        cmd = "./build_all -o release -j 4 BEAMS3D"
        # subprocess.Popen(cmd, shell=True, env=os.environ, cwd=os.getcwd())
        subprocess.Popen(cmd, shell=True)
