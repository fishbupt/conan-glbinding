#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools


class GlBindingConan(ConanFile):
    name = "glbinding"
    version = "3.0.2"
    description = "Cross platform C++ binding for the OpenGL API."
    url = ""
    homepage = "https://github.com/cginternals/glbinding"
    author = "fishbupt <fishbupt@gmail.com>"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    extracted_dir = "glbinding-" + version
    no_copy_source = True
    generators = "cmake"
    requires = ("glfw/[^3.2.1]@bincrafters/stable")

    def source(self):
        source_url = "https://github.com/cginternals/glbinding"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))

        tools.replace_in_file("{}/CMakeLists.txt".format(self.extracted_dir), "project(${META_PROJECT_NAME} C CXX)",
                              '''project(${META_PROJECT_NAME} C CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
        cmake.definitions["OPTION_BUILD_TEST"] = "OFF"
        cmake.definitions["OPTION_BUILD_DOCS"] = "OFF"
        cmake.definitions["OPTION_BUILD_TOOLS"] = "ON"
        cmake.definitions["OPTION_BUILD_EXAMPLES"] = "OFF"
        cmake.configure(source_folder=self.extracted_dir)
        cmake.build()
        cmake.install()

    def package(self):
        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=".", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=".", keep_path=False)
        

    def package_info(self):
        if self.settings.build_type == 'Debug':
            self.cpp_info.libs = ["glbindingd", "glbinding-auxd"]
        else:
            self.cpp_info.libs = ["glbinding", "glbinding-aux"]
