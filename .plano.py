import os

from plano import *

@command
def install():
    install_proton()
    install_router()

@command
def install_proton():
    if not exists("qpid-proton"):
        run("git clone --depth 1 https://github.com/apache/qpid-proton.git")

    cmake_options = [
        "--fresh", # Always reconfigure
        "-DCMAKE_BUILD_TYPE=RelWithDebInfo",
        "-DCMAKE_INSTALL_PREFIX=~/.local",
        "-DBUILD_TLS=ON",
        "-DBUILD_CPP=OFF",
        "-DBUILD_GO=OFF",
        "-DBUILD_PYTHON=OFF",
        "-DBUILD_RUBY=OFF",
    ]

    cmake_options = " ".join(cmake_options)

    remove("qpid-proton-build")

    with working_dir("qpid-proton-build"):
        print()
        print("PROFILE GENERATE")
        print()

        with working_env(CFLAGS="-fprofile-generate -Wno-error=missing-profile"):
            run(f"cmake ../qpid-proton {cmake_options}")

        run(f"make -j {os.cpu_count()}")

        # run("make install")
        # with working_dir("/home/jross/code/queequeg"):
        #     with working_env(LD_LIBRARY_PATH="/home/jross/.local/lib64"):
        #         run("./plano record")

        run("ctest -R '^c-' -E c-fdlimit-tests")

        print()
        print("PROFILE USE")
        print()

        with working_env(CFLAGS="-fprofile-use -fprofile-correction -Wno-error=missing-profile"):
            run(f"cmake ../qpid-proton {cmake_options}")

        run(f"make -j {os.cpu_count()}")
        run("make install")

@command
def install_router():
    if not exists("skupper-router"):
        run("git clone --depth 1 https://github.com/skupperproject/skupper-router.git")

    cmake_options = [
        "--fresh", # Always reconfigure
        "-DCMAKE_BUILD_TYPE=RelWithDebInfo",
        "-DCMAKE_INSTALL_PREFIX=~/.local",
    ]

    cmake_options = " ".join(cmake_options)

    remove("skupper-router-build")

    with working_dir("skupper-router-build"):
        print()
        print("PROFILE GENERATE")
        print()

        with working_env(CFLAGS="-fprofile-generate -Wno-error=missing-profile -Wno-error=format-truncation"):
            run(f"cmake ../skupper-router {cmake_options}")

        run(f"make -j {os.cpu_count()}")

        # run("make install")
        # with working_dir("/home/jross/code/flimflam"):
        #     with working_env(LD_LIBRARY_PATH="/home/jross/.local/lib64"):
        #         run("./plano skstat --buffer 16385")

        run("ctest -R '^unit_tests$'")

        print()
        print("PROFILE USE")
        print()

        with working_env(CFLAGS="-fprofile-use -fprofile-correction -Wno-error=missing-profile -Wno-error=format-truncation"):
            run(f"cmake ../skupper-router {cmake_options}")

        run(f"make -j {os.cpu_count()}")
        run("make install")


# /home/jross/code/puggo/skupper-router/tests/field_test.c:270:85: error: ‘%s’ directive argument is null []8;;https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html#index-Wformat-truncation=-Werror=format-truncation=]8;;]
#   270 |         snprintf(fail_text, FAIL_TEXT_SIZE, "Addr '%s' failed.  Expected '%s', got '%s'",
#       |                                                                                     ^~
