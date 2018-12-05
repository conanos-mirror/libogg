from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from conanos.build import config_scheme
import os

class LiboggConan(ConanFile):
    name = "libogg"
    version = "1.3.3"
    description = "The OGG library"
    url = "https://github.com/bincrafters/conan-ogg"
    homepage = "https://github.com/xiph/ogg"
    license = "BSD"
    exports = ["LICENSE.md", "FindOGG.cmake",'ogg.pc.in']
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    source_subfolder = "source_subfolder"
    settings = "os", "arch", "build_type", "compiler"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=True", "fPIC=True"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        del self.settings.compiler.libcxx
        config_scheme(self)

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = 'ogg' + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        import shutil
        shutil.copy('ogg.pc.in',os.path.join(self.source_subfolder,'ogg.pc.in'))

    @property
    def _msvc(self):
        return self.settings.compiler == 'Visual Studio'

    def build(self):
        if self._msvc:
            self.cmake_build()
        else:
            self.gcc_build()


    def cmake_build(self):
        cmake = CMake(self)
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.configure(build_folder='~build')
        cmake.build()
        cmake.install()        

    def gcc_build(self):
        with tools.chdir(self.source_subfolder):
            self.run("autoreconf -f -i")

            autotools = AutoToolsBuildEnvironment(self)
            _args = ["--prefix=%s/builddir/install"%(os.getcwd()), "--enable-introspection"]
            if self.options.shared:
                _args.extend(['--enable-shared=yes','--enable-static=no'])
            else:
                _args.extend(['--enable-shared=no','--enable-static=yes'])
            autotools.configure(args=_args)
            autotools.make(args=["-j2"])
            autotools.install()

    def package(self):
        self.copy("FindOGG.cmake")
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir/install"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

