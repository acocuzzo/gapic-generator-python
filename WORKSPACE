workspace(name = "gapic_generator_python")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

_bazel_skylib_version = "1.4.0"

_bazel_skylib_sha256 = "f24ab666394232f834f74d19e2ff142b0af17466ea0c69a3f4c276ee75f6efce"

http_archive(
    name = "bazel_skylib",
    sha256 = _bazel_skylib_sha256,
    url = "https://github.com/bazelbuild/bazel-skylib/releases/download/{0}/bazel-skylib-{0}.tar.gz".format(_bazel_skylib_version),
)

_io_bazel_rules_go_version = "0.33.0"
http_archive(
    name = "io_bazel_rules_go",
    sha256 = "685052b498b6ddfe562ca7a97736741d87916fe536623afb7da2824c0211c369",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/rules_go/releases/download/v{0}/rules_go-v{0}.zip".format(_io_bazel_rules_go_version),
        "https://github.com/bazelbuild/rules_go/releases/download/v{0}/rules_go-v{0}.zip".format(_io_bazel_rules_go_version),
    ],
)

_rules_python_version = "0.26.0"

_rules_python_sha256 = "9d04041ac92a0985e344235f5d946f71ac543f1b1565f2cdbc9a2aaee8adf55b"

http_archive(
    name = "rules_python",
    sha256 = _rules_python_sha256,
    strip_prefix = "rules_python-{}".format(_rules_python_version),
    url = "https://github.com/bazelbuild/rules_python/archive/{}.tar.gz".format(_rules_python_version),
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

load("@rules_python//python:pip.bzl", "pip_parse")


pip_parse(
    name = "gapic_generator_python_pip_deps",
	requirements_lock = "//:requirements.txt",
)
load("@gapic_generator_python_pip_deps//:requirements.bzl", "install_deps")

install_deps()
#
# Import gapic-generator-python specific dependencies
#
load(
    "//:repositories.bzl",
    "gapic_generator_python",
    "gapic_generator_register_toolchains",
)

gapic_generator_python()

gapic_generator_register_toolchains()

# TODO(https://github.com/googleapis/gapic-generator-python/issues/1781):
# Remove this import once gRPC depends on a newer version.
#
# Background: Import boringssl explicitly to override what gRPC
# imports as its dependency.  Boringssl build fails on gcc12 without
# this fix:
# https://github.com/google/boringssl/commit/8462a367bb57e9524c3d8eca9c62733c63a63cf4,
# which is present only in the newest version of boringssl, not the
# one imported by gRPC.
http_archive(
    name = "boringssl",
    sha256 = "b460f8673f3393e58ce506e9cdde7f2c3b2575b075f214cb819fb57d809f052b",
    strip_prefix = "boringssl-bb41bc007079982da419c0ec3186e510cbcf09d0",
    urls = [
        "https://github.com/google/boringssl/archive/bb41bc007079982da419c0ec3186e510cbcf09d0.zip",
    ],
)

_grpc_version = "1.55.1"

_grpc_sha256 = "17c0685da231917a7b3be2671a7b13b550a85fdda5e475313264c5f51c4da3f8"

http_archive(
    name = "com_github_grpc_grpc",
    sha256 = _grpc_sha256,
    strip_prefix = "grpc-%s" % _grpc_version,
    urls = ["https://github.com/grpc/grpc/archive/v%s.zip" % _grpc_version],
)
# instantiated in grpc_deps().
http_archive(
    name = "com_google_protobuf",
    sha256 = "0b0395d34e000f1229679e10d984ed7913078f3dd7f26cf0476467f5e65716f4",
    strip_prefix = "protobuf-23.2",
    urls = ["https://github.com/protocolbuffers/protobuf/archive/v23.2.tar.gz"],
)
load("@com_github_grpc_grpc//bazel:grpc_deps.bzl", "grpc_deps")

grpc_deps()

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps", "PROTOBUF_MAVEN_ARTIFACTS")
# This is actually already done within grpc_deps but calling this for Bazel convention.
protobuf_deps()

# gRPC enforces a specific version of Go toolchain which conflicts with our build.
# All the relevant parts of grpc_extra_deps() are imported in this  WORKSPACE file
# explicitly, that is why we do not call grpc_extra_deps() here and call
# apple_rules_dependencies and apple_support_dependencies macros explicitly.

load("@build_bazel_rules_apple//apple:repositories.bzl", "apple_rules_dependencies")

apple_rules_dependencies()

load("@build_bazel_apple_support//lib:repositories.bzl", "apple_support_dependencies")

apple_support_dependencies()

load("@com_google_googleapis//:repository_rules.bzl", "switched_rules_by_language")

switched_rules_by_language(
    name = "com_google_googleapis_imports",
    gapic = True,
    grpc = True,
)
