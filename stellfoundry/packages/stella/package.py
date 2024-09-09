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
#     spack install stella
#
# You can edit this file again by typing:
#
#     spack edit stella
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *
import os


class Stella(CMakePackage):
    """stella is a flux tube gyrokinetic code for micro-stability and turbulence simulations of strongly magnetised plasma."""

    homepage = "https://github.com/stellaGK/stella/"
    git = "https://github.com/jychoi-hpc/stella.git"

    maintainers("github_user1", "github_user2")

    # FIXME: Add proper versions here.
    # version("1.2.4")
    version("dev-adios", branch="dev-adios")

    # FIXME: Add dependencies if required.
    depends_on("fftw")
    depends_on("netcdf-fortran")
    depends_on("adios2@2.9.2+fortran+mpi~blosc2~bzip2~sst~sz~zfp~mgard~libcatalyst~png")

    def setup_build_environment(self, env):
        env.set("FFLAGS", "-fallow-argument-mismatch")

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(os.path.join(self.build_directory, "stella"), prefix.bin)

