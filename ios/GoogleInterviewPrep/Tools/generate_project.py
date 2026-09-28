import os
import glob
import hashlib

def gen_id(name):
    # Deterministic 24-char hex ID from string
    h = hashlib.md5(name.encode('utf-8')).hexdigest()[:24].upper()
    return h

project_dir = "ios/GoogleInterviewPrep"
proj_path = f"{project_dir}/GoogleInterviewPrep.xcodeproj"
os.makedirs(proj_path, exist_ok=True)
schemes_dir = f"{proj_path}/xcshareddata/xcschemes"
os.makedirs(schemes_dir, exist_ok=True)

# Collect files
def get_rel_files(subpath):
    full = os.path.join(project_dir, subpath)
    res = []
    for root, dirs, files in os.walk(full):
        asset_catalogs = sorted(d for d in dirs if d.endswith('.xcassets'))
        for catalog in asset_catalogs:
            rel = os.path.relpath(os.path.join(root, catalog), project_dir)
            res.append(rel)
        dirs[:] = [d for d in dirs if not d.endswith('.xcassets')]
        for f in sorted(files):
            if f.endswith('.DS_Store'): continue
            rel = os.path.relpath(os.path.join(root, f), project_dir)
            res.append(rel)
    return sorted(res)

app_swift_files = [f for f in get_rel_files("GoogleInterviewPrep") if f.endswith(".swift")]
app_resource_files = [f for f in get_rel_files("GoogleInterviewPrep/Resources")]
test_files = [f for f in get_rel_files("GoogleInterviewPrepTests") if f.endswith(".swift")]
uitest_files = [f for f in get_rel_files("GoogleInterviewPrepUITests") if f.endswith(".swift")]

print(f"Found {len(app_swift_files)} App Swift files")
print(f"Found {len(app_resource_files)} App resource files")
print(f"Found {len(test_files)} Unit test files")
print(f"Found {len(uitest_files)} UI test files")

# File references and build files
pbx_filerefs = []
pbx_buildfiles = []

app_source_build_ids = []
app_resource_build_ids = []
test_source_build_ids = []
uitest_source_build_ids = []

def file_type_for_ext(ext):
    types = {
        'swift': 'sourcecode.swift',
        'json': 'text.json',
        'html': 'text.html',
        'css': 'text.css',
        'js': 'sourcecode.javascript',
        'md': 'net.daringfireball.markdown',
        'java': 'sourcecode.java',
        'plist': 'text.plist.xml',
        'xcassets': 'folder.assetcatalog'
    }
    return types.get(ext, 'text')

all_registered_files = {}

def add_file(rel_path, is_resource=False, is_test=False, is_uitest=False):
    f_id = gen_id(f"FILEREF_{rel_path}")
    b_id = gen_id(f"BUILDFILE_{rel_path}")
    fname = os.path.basename(rel_path)
    ext = fname.split('.')[-1]
    ftype = file_type_for_ext(ext)
    
    fileref_entry = f'\t\t{f_id} /* {fname} */ = {{isa = PBXFileReference; lastKnownFileType = {ftype}; name = "{fname}"; path = "{rel_path}"; sourceTree = "<group>"; }};'
    pbx_filerefs.append(fileref_entry)
    all_registered_files[rel_path] = f_id
    
    if ext == 'swift':
        buildfile_entry = f'\t\t{b_id} /* {fname} in Sources */ = {{isa = PBXBuildFile; fileRef = {f_id} /* {fname} */; }};'
        pbx_buildfiles.append(buildfile_entry)
        if is_test:
            test_source_build_ids.append(b_id)
        elif is_uitest:
            uitest_source_build_ids.append(b_id)
        else:
            app_source_build_ids.append(b_id)
    elif is_resource:
        buildfile_entry = f'\t\t{b_id} /* {fname} in Resources */ = {{isa = PBXBuildFile; fileRef = {f_id} /* {fname} */; }};'
        pbx_buildfiles.append(buildfile_entry)
        app_resource_build_ids.append(b_id)

for f in app_swift_files:
    add_file(f)

for f in app_resource_files:
    add_file(f, is_resource=True)

for f in test_files:
    add_file(f, is_test=True)

for f in uitest_files:
    add_file(f, is_uitest=True)

# Add plists
add_file("GoogleInterviewPrep/Info.plist")
add_file("GoogleInterviewPrepTests/Info.plist")
add_file("GoogleInterviewPrepUITests/Info.plist")

# Products
app_product_fileref = gen_id("PRODUCT_APP")
test_product_fileref = gen_id("PRODUCT_TEST")
uitest_product_fileref = gen_id("PRODUCT_UITEST")

pbx_filerefs.append(f'\t\t{app_product_fileref} /* GoogleInterviewPrep.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = GoogleInterviewPrep.app; sourceTree = BUILT_PRODUCTS_DIR; }};')
pbx_filerefs.append(f'\t\t{test_product_fileref} /* GoogleInterviewPrepTests.xctest */ = {{isa = PBXFileReference; explicitFileType = wrapper.cfbundle; includeInIndex = 0; path = GoogleInterviewPrepTests.xctest; sourceTree = BUILT_PRODUCTS_DIR; }};')
pbx_filerefs.append(f'\t\t{uitest_product_fileref} /* GoogleInterviewPrepUITests.xctest */ = {{isa = PBXFileReference; explicitFileType = wrapper.cfbundle; includeInIndex = 0; path = GoogleInterviewPrepUITests.xctest; sourceTree = BUILT_PRODUCTS_DIR; }};')

# Group hierarchy
root_group_id = gen_id("ROOT_GROUP")
app_group_id = gen_id("APP_GROUP")
test_group_id = gen_id("TEST_GROUP")
uitest_group_id = gen_id("UITEST_GROUP")
products_group_id = gen_id("PRODUCTS_GROUP")

def make_group_children(file_list):
    res = []
    for f in file_list:
        fid = all_registered_files[f]
        fname = os.path.basename(f)
        res.append(f'\t\t\t\t{fid} /* {fname} */,')
    return "\n".join(res)

app_children = make_group_children(app_swift_files + app_resource_files + ["GoogleInterviewPrep/Info.plist"])
test_children = make_group_children(test_files + ["GoogleInterviewPrepTests/Info.plist"])
uitest_children = make_group_children(uitest_files + ["GoogleInterviewPrepUITests/Info.plist"])

groups = f"""
\t\t{root_group_id} = {{
\t\t\tisa = PBXGroup;
\t\t\tchildren = (
\t\t\t\t{app_group_id} /* GoogleInterviewPrep */,
\t\t\t\t{test_group_id} /* GoogleInterviewPrepTests */,
\t\t\t\t{uitest_group_id} /* GoogleInterviewPrepUITests */,
\t\t\t\t{products_group_id} /* Products */,
\t\t\t);
\t\t\tsourceTree = "<group>";
\t\t}};
\t\t{app_group_id} = {{
\t\t\tisa = PBXGroup;
\t\t\tchildren = (
{app_children}
\t\t\t);
\t\t\tname = GoogleInterviewPrep;
\t\t\tsourceTree = "<group>";
\t\t}};
\t\t{test_group_id} = {{
\t\t\tisa = PBXGroup;
\t\t\tchildren = (
{test_children}
\t\t\t);
\t\t\tname = GoogleInterviewPrepTests;
\t\t\tsourceTree = "<group>";
\t\t}};
\t\t{uitest_group_id} = {{
\t\t\tisa = PBXGroup;
\t\t\tchildren = (
{uitest_children}
\t\t\t);
\t\t\tname = GoogleInterviewPrepUITests;
\t\t\tsourceTree = "<group>";
\t\t}};
\t\t{products_group_id} = {{
\t\t\tisa = PBXGroup;
\t\t\tchildren = (
\t\t\t\t{app_product_fileref} /* GoogleInterviewPrep.app */,
\t\t\t\t{test_product_fileref} /* GoogleInterviewPrepTests.xctest */,
\t\t\t\t{uitest_product_fileref} /* GoogleInterviewPrepUITests.xctest */,
\t\t\t);
\t\t\tname = Products;
\t\t\tsourceTree = "<group>";
\t\t}};
"""

# Targets
app_target_id = gen_id("TARGET_APP")
test_target_id = gen_id("TARGET_TEST")
uitest_target_id = gen_id("TARGET_UITEST")

# Build Phases
app_sources_id = gen_id("PHASE_APP_SOURCES")
app_resources_id = gen_id("PHASE_APP_RESOURCES")
app_frameworks_id = gen_id("PHASE_APP_FRAMEWORKS")

test_sources_id = gen_id("PHASE_TEST_SOURCES")
test_frameworks_id = gen_id("PHASE_TEST_FRAMEWORKS")
test_resources_id = gen_id("PHASE_TEST_RESOURCES")

uitest_sources_id = gen_id("PHASE_UITEST_SOURCES")
uitest_frameworks_id = gen_id("PHASE_UITEST_FRAMEWORKS")
uitest_resources_id = gen_id("PHASE_UITEST_RESOURCES")

# Target Dependencies for Tests
test_dependency_id = gen_id("DEP_TEST_APP")
test_proxy_id = gen_id("PROXY_TEST_APP")
uitest_dependency_id = gen_id("DEP_UITEST_APP")
uitest_proxy_id = gen_id("PROXY_UITEST_APP")

dependencies = f"""
\t\t{test_proxy_id} /* PBXContainerItemProxy */ = {{
\t\t\tisa = PBXContainerItemProxy;
\t\t\tcontainerPortal = {gen_id('PROJECT')};
\t\t\tproxyType = 1;
\t\t\tremoteGlobalIDString = {app_target_id};
\t\t\tremoteInfo = GoogleInterviewPrep;
\t\t}};
\t\t{test_dependency_id} /* PBXTargetDependency */ = {{
\t\t\tisa = PBXTargetDependency;
\t\t\ttarget = {app_target_id};
\t\t\ttargetProxy = {test_proxy_id} /* PBXContainerItemProxy */;
\t\t}};
\t\t{uitest_proxy_id} /* PBXContainerItemProxy */ = {{
\t\t\tisa = PBXContainerItemProxy;
\t\t\tcontainerPortal = {gen_id('PROJECT')};
\t\t\tproxyType = 1;
\t\t\tremoteGlobalIDString = {app_target_id};
\t\t\tremoteInfo = GoogleInterviewPrep;
\t\t}};
\t\t{uitest_dependency_id} /* PBXTargetDependency */ = {{
\t\t\tisa = PBXTargetDependency;
\t\t\ttarget = {app_target_id};
\t\t\ttargetProxy = {uitest_proxy_id} /* PBXContainerItemProxy */;
\t\t}};
"""

# Format build phases
def format_build_ids(ids):
    return "\n".join([f"\t\t\t\t{i}," for i in ids])

build_phases = f"""
\t\t{app_sources_id} /* Sources */ = {{
\t\t\tisa = PBXSourcesBuildPhase;
\t\t\tbuildActionMask = 2147483647;
\t\t\tfiles = (
{format_build_ids(app_source_build_ids)}
\t\t\t);
\t\t\trunOnlyForDeploymentPostprocessing = 0;
\t\t}};
\t\t{app_resources_id} /* Resources */ = {{
\t\t\tisa = PBXResourcesBuildPhase;
\t\t\tbuildActionMask = 2147483647;
\t\t\tfiles = (
{format_build_ids(app_resource_build_ids)}
\t\t\t);
\t\t\trunOnlyForDeploymentPostprocessing = 0;
\t\t}};
\t\t{app_frameworks_id} /* Frameworks */ = {{
\t\t\tisa = PBXFrameworksBuildPhase;
\t\t\tbuildActionMask = 2147483647;
\t\t\tfiles = ();
\t\t\trunOnlyForDeploymentPostprocessing = 0;
\t\t}};
\t\t{test_sources_id} /* Sources */ = {{
\t\t\tisa = PBXSourcesBuildPhase;
\t\t\tbuildActionMask = 2147483647;
\t\t\tfiles = (
{format_build_ids(test_source_build_ids)}
\t\t\t);
\t\t\trunOnlyForDeploymentPostprocessing = 0;
\t\t}};
\t\t{test_resources_id} /* Resources */ = {{
\t\t\tisa = PBXResourcesBuildPhase;
\t\t\tbuildActionMask = 2147483647;
\t\t\tfiles = ();
\t\t\trunOnlyForDeploymentPostprocessing = 0;
\t\t}};
\t\t{test_frameworks_id} /* Frameworks */ = {{
\t\t\tisa = PBXFrameworksBuildPhase;
\t\t\tbuildActionMask = 2147483647;
\t\t\tfiles = ();
\t\t\trunOnlyForDeploymentPostprocessing = 0;
\t\t}};
\t\t{uitest_sources_id} /* Sources */ = {{
\t\t\tisa = PBXSourcesBuildPhase;
\t\t\tbuildActionMask = 2147483647;
\t\t\tfiles = (
{format_build_ids(uitest_source_build_ids)}
\t\t\t);
\t\t\trunOnlyForDeploymentPostprocessing = 0;
\t\t}};
\t\t{uitest_resources_id} /* Resources */ = {{
\t\t\tisa = PBXResourcesBuildPhase;
\t\t\tbuildActionMask = 2147483647;
\t\t\tfiles = ();
\t\t\trunOnlyForDeploymentPostprocessing = 0;
\t\t}};
\t\t{uitest_frameworks_id} /* Frameworks */ = {{
\t\t\tisa = PBXFrameworksBuildPhase;
\t\t\tbuildActionMask = 2147483647;
\t\t\tfiles = ();
\t\t\trunOnlyForDeploymentPostprocessing = 0;
\t\t}};
"""

# Configuration lists
proj_cfg_list = gen_id("CFG_PROJ_LIST")
app_cfg_list = gen_id("CFG_APP_LIST")
test_cfg_list = gen_id("CFG_TEST_LIST")
uitest_cfg_list = gen_id("CFG_UITEST_LIST")

proj_dbg_cfg = gen_id("CFG_PROJ_DBG")
proj_rel_cfg = gen_id("CFG_PROJ_REL")
app_dbg_cfg = gen_id("CFG_APP_DBG")
app_rel_cfg = gen_id("CFG_APP_REL")
test_dbg_cfg = gen_id("CFG_TEST_DBG")
test_rel_cfg = gen_id("CFG_TEST_REL")
uitest_dbg_cfg = gen_id("CFG_UITEST_DBG")
uitest_rel_cfg = gen_id("CFG_UITEST_REL")

configs = f"""
\t\t{proj_dbg_cfg} /* Debug */ = {{
\t\t\tisa = XCBuildConfiguration;
\t\t\tbuildSettings = {{
\t\t\t\tALWAYS_SEARCH_USER_PATHS = NO;
\t\t\t\tCLANG_ANALYZER_NONNULL = YES;
\t\t\t\tCLANG_ENABLE_MODULES = YES;
\t\t\t\tCLANG_ENABLE_OBJC_ARC = YES;
\t\t\t\tCOPY_PHASE_STRIP = NO;
\t\t\t\tDEBUG_INFORMATION_FORMAT = dwarf;
\t\t\t\tENABLE_STRICT_OBJC_MSGSEND = YES;
\t\t\t\tENABLE_TESTABILITY = YES;
\t\t\t\tGCC_OPTIMIZATION_LEVEL = 0;
\t\t\t\tGCC_PREPROCESSOR_DEFINITIONS = (
\t\t\t\t\t"DEBUG=1",
\t\t\t\t\t"$(inherited)",
\t\t\t\t);
\t\t\t\tIPHONEOS_DEPLOYMENT_TARGET = 16.4;
\t\t\t\tMTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE;
\t\t\t\tONLY_ACTIVE_ARCH = YES;
\t\t\t\tSDKROOT = iphoneos;
\t\t\t\tSWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG;
\t\t\t\tSWIFT_OPTIMIZATION_LEVEL = "-Onone";
\t\t\t\tSWIFT_VERSION = 6.0;
\t\t\t}};
\t\t\tname = Debug;
\t\t}};
\t\t{proj_rel_cfg} /* Release */ = {{
\t\t\tisa = XCBuildConfiguration;
\t\t\tbuildSettings = {{
\t\t\t\tALWAYS_SEARCH_USER_PATHS = NO;
\t\t\t\tCLANG_ANALYZER_NONNULL = YES;
\t\t\t\tCLANG_ENABLE_MODULES = YES;
\t\t\t\tCLANG_ENABLE_OBJC_ARC = YES;
\t\t\t\tCOPY_PHASE_STRIP = NO;
\t\t\t\tDEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
\t\t\t\tENABLE_NS_ASSERTIONS = NO;
\t\t\t\tENABLE_STRICT_OBJC_MSGSEND = YES;
\t\t\t\tIPHONEOS_DEPLOYMENT_TARGET = 16.4;
\t\t\t\tMTL_ENABLE_DEBUG_INFO = NO;
\t\t\t\tSDKROOT = iphoneos;
\t\t\t\tSWIFT_COMPILATION_MODE = wholemodule;
\t\t\t\tSWIFT_OPTIMIZATION_LEVEL = "-O";
\t\t\t\tSWIFT_VERSION = 6.0;
\t\t\t\tVALIDATE_PRODUCT = YES;
\t\t\t}};
\t\t\tname = Release;
\t\t}};
\t\t{app_dbg_cfg} /* Debug */ = {{
\t\t\tisa = XCBuildConfiguration;
\t\t\tbuildSettings = {{
\t\t\t\tASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
\t\t\t\tCODE_SIGN_STYLE = Automatic;
\t\t\t\tCURRENT_PROJECT_VERSION = 1;
\t\t\t\tGENERATE_INFOPLIST_FILE = NO;
\t\t\t\tINFOPLIST_FILE = GoogleInterviewPrep/Info.plist;
\t\t\t\tLD_RUNPATH_SEARCH_PATHS = (
\t\t\t\t\t"$(inherited)",
\t\t\t\t\t"@executable_path/Frameworks",
\t\t\t\t);
\t\t\t\tMARKETING_VERSION = 1.0.0;
\t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = dev.apoorv.GoogleInterviewPrep;
\t\t\t\tPRODUCT_NAME = "$(TARGET_NAME)";
\t\t\t\tSWIFT_EMIT_LOC_STRINGS = YES;
\t\t\t\tTARGETED_DEVICE_FAMILY = "1,2";
\t\t\t}};
\t\t\tname = Debug;
\t\t}};
\t\t{app_rel_cfg} /* Release */ = {{
\t\t\tisa = XCBuildConfiguration;
\t\t\tbuildSettings = {{
\t\t\t\tASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
\t\t\t\tCODE_SIGN_STYLE = Automatic;
\t\t\t\tCURRENT_PROJECT_VERSION = 1;
\t\t\t\tGENERATE_INFOPLIST_FILE = NO;
\t\t\t\tINFOPLIST_FILE = GoogleInterviewPrep/Info.plist;
\t\t\t\tLD_RUNPATH_SEARCH_PATHS = (
\t\t\t\t\t"$(inherited)",
\t\t\t\t\t"@executable_path/Frameworks",
\t\t\t\t);
\t\t\t\tMARKETING_VERSION = 1.0.0;
\t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = dev.apoorv.GoogleInterviewPrep;
\t\t\t\tPRODUCT_NAME = "$(TARGET_NAME)";
\t\t\t\tSWIFT_EMIT_LOC_STRINGS = YES;
\t\t\t\tTARGETED_DEVICE_FAMILY = "1,2";
\t\t\t}};
\t\t\tname = Release;
\t\t}};
\t\t{test_dbg_cfg} /* Debug */ = {{
\t\t\tisa = XCBuildConfiguration;
\t\t\tbuildSettings = {{
\t\t\t\tALWAYS_EMBED_SWIFT_STANDARD_LIBRARIES = YES;
\t\t\t\tBUNDLE_LOADER = "$(TEST_HOST)";
\t\t\t\tCODE_SIGN_STYLE = Automatic;
\t\t\t\tCURRENT_PROJECT_VERSION = 1;
\t\t\t\tGENERATE_INFOPLIST_FILE = NO;
\t\t\t\tINFOPLIST_FILE = GoogleInterviewPrepTests/Info.plist;
\t\t\t\tMARKETING_VERSION = 1.0;
\t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = dev.apoorv.GoogleInterviewPrepTests;
\t\t\t\tPRODUCT_NAME = "$(TARGET_NAME)";
\t\t\t\tTARGETED_DEVICE_FAMILY = "1,2";
\t\t\t\tTEST_HOST = "$(BUILT_PRODUCTS_DIR)/GoogleInterviewPrep.app/$(BUNDLE_EXECUTABLE_FOLDER_PATH)/GoogleInterviewPrep";
\t\t\t}};
\t\t\tname = Debug;
\t\t}};
\t\t{test_rel_cfg} /* Release */ = {{
\t\t\tisa = XCBuildConfiguration;
\t\t\tbuildSettings = {{
\t\t\t\tALWAYS_EMBED_SWIFT_STANDARD_LIBRARIES = YES;
\t\t\t\tBUNDLE_LOADER = "$(TEST_HOST)";
\t\t\t\tCODE_SIGN_STYLE = Automatic;
\t\t\t\tCURRENT_PROJECT_VERSION = 1;
\t\t\t\tGENERATE_INFOPLIST_FILE = NO;
\t\t\t\tINFOPLIST_FILE = GoogleInterviewPrepTests/Info.plist;
\t\t\t\tMARKETING_VERSION = 1.0;
\t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = dev.apoorv.GoogleInterviewPrepTests;
\t\t\t\tPRODUCT_NAME = "$(TARGET_NAME)";
\t\t\t\tTARGETED_DEVICE_FAMILY = "1,2";
\t\t\t\tTEST_HOST = "$(BUILT_PRODUCTS_DIR)/GoogleInterviewPrep.app/$(BUNDLE_EXECUTABLE_FOLDER_PATH)/GoogleInterviewPrep";
\t\t\t}};
\t\t\tname = Release;
\t\t}};
\t\t{uitest_dbg_cfg} /* Debug */ = {{
\t\t\tisa = XCBuildConfiguration;
\t\t\tbuildSettings = {{
\t\t\t\tALWAYS_EMBED_SWIFT_STANDARD_LIBRARIES = YES;
\t\t\t\tCODE_SIGN_STYLE = Automatic;
\t\t\t\tCURRENT_PROJECT_VERSION = 1;
\t\t\t\tGENERATE_INFOPLIST_FILE = NO;
\t\t\t\tINFOPLIST_FILE = GoogleInterviewPrepUITests/Info.plist;
\t\t\t\tMARKETING_VERSION = 1.0;
\t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = dev.apoorv.GoogleInterviewPrepUITests;
\t\t\t\tPRODUCT_NAME = "$(TARGET_NAME)";
\t\t\t\tTARGETED_DEVICE_FAMILY = "1,2";
\t\t\t\tTEST_TARGET_NAME = GoogleInterviewPrep;
\t\t\t}};
\t\t\tname = Debug;
\t\t}};
\t\t{uitest_rel_cfg} /* Release */ = {{
\t\t\tisa = XCBuildConfiguration;
\t\t\tbuildSettings = {{
\t\t\t\tALWAYS_EMBED_SWIFT_STANDARD_LIBRARIES = YES;
\t\t\t\tCODE_SIGN_STYLE = Automatic;
\t\t\t\tCURRENT_PROJECT_VERSION = 1;
\t\t\t\tGENERATE_INFOPLIST_FILE = NO;
\t\t\t\tINFOPLIST_FILE = GoogleInterviewPrepUITests/Info.plist;
\t\t\t\tMARKETING_VERSION = 1.0;
\t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = dev.apoorv.GoogleInterviewPrepUITests;
\t\t\t\tPRODUCT_NAME = "$(TARGET_NAME)";
\t\t\t\tTARGETED_DEVICE_FAMILY = "1,2";
\t\t\t\tTEST_TARGET_NAME = GoogleInterviewPrep;
\t\t\t}};
\t\t\tname = Release;
\t\t}};

\t\t{proj_cfg_list} /* Build configuration list for PBXProject */ = {{
\t\t\tisa = XCConfigurationList;
\t\t\tbuildConfigurations = (
\t\t\t\t{proj_dbg_cfg} /* Debug */,
\t\t\t\t{proj_rel_cfg} /* Release */,
\t\t\t);
\t\t\tdefaultConfigurationIsVisible = 0;
\t\t\tdefaultConfigurationName = Release;
\t\t}};
\t\t{app_cfg_list} /* Build configuration list for PBXNativeTarget "GoogleInterviewPrep" */ = {{
\t\t\tisa = XCConfigurationList;
\t\t\tbuildConfigurations = (
\t\t\t\t{app_dbg_cfg} /* Debug */,
\t\t\t\t{app_rel_cfg} /* Release */,
\t\t\t);
\t\t\tdefaultConfigurationIsVisible = 0;
\t\t\tdefaultConfigurationName = Release;
\t\t}};
\t\t{test_cfg_list} /* Build configuration list for PBXNativeTarget "GoogleInterviewPrepTests" */ = {{
\t\t\tisa = XCConfigurationList;
\t\t\tbuildConfigurations = (
\t\t\t\t{test_dbg_cfg} /* Debug */,
\t\t\t\t{test_rel_cfg} /* Release */,
\t\t\t);
\t\t\tdefaultConfigurationIsVisible = 0;
\t\t\tdefaultConfigurationName = Release;
\t\t}};
\t\t{uitest_cfg_list} /* Build configuration list for PBXNativeTarget "GoogleInterviewPrepUITests" */ = {{
\t\t\tisa = XCConfigurationList;
\t\t\tbuildConfigurations = (
\t\t\t\t{uitest_dbg_cfg} /* Debug */,
\t\t\t\t{uitest_rel_cfg} /* Release */,
\t\t\t);
\t\t\tdefaultConfigurationIsVisible = 0;
\t\t\tdefaultConfigurationName = Release;
\t\t}};
"""

# Native Targets
targets = f"""
\t\t{app_target_id} /* GoogleInterviewPrep */ = {{
\t\t\tisa = PBXNativeTarget;
\t\t\tbuildConfigurationList = {app_cfg_list} /* Build configuration list */;
\t\t\tbuildPhases = (
\t\t\t\t{app_sources_id} /* Sources */,
\t\t\t\t{app_frameworks_id} /* Frameworks */,
\t\t\t\t{app_resources_id} /* Resources */,
\t\t\t);
\t\t\tbuildRules = ();
\t\t\tdependencies = ();
\t\t\tname = GoogleInterviewPrep;
\t\t\tproductName = GoogleInterviewPrep;
\t\t\tproductReference = {app_product_fileref} /* GoogleInterviewPrep.app */;
\t\t\tproductType = "com.apple.product-type.application";
\t\t}};
\t\t{test_target_id} /* GoogleInterviewPrepTests */ = {{
\t\t\tisa = PBXNativeTarget;
\t\t\tbuildConfigurationList = {test_cfg_list} /* Build configuration list */;
\t\t\tbuildPhases = (
\t\t\t\t{test_sources_id} /* Sources */,
\t\t\t\t{test_frameworks_id} /* Frameworks */,
\t\t\t\t{test_resources_id} /* Resources */,
\t\t\t);
\t\t\tbuildRules = ();
\t\t\tdependencies = (
\t\t\t\t{test_dependency_id} /* PBXTargetDependency */,
\t\t\t);
\t\t\tname = GoogleInterviewPrepTests;
\t\t\tproductName = GoogleInterviewPrepTests;
\t\t\tproductReference = {test_product_fileref} /* GoogleInterviewPrepTests.xctest */;
\t\t\tproductType = "com.apple.product-type.bundle.unit-test";
\t\t}};
\t\t{uitest_target_id} /* GoogleInterviewPrepUITests */ = {{
\t\t\tisa = PBXNativeTarget;
\t\t\tbuildConfigurationList = {uitest_cfg_list} /* Build configuration list */;
\t\t\tbuildPhases = (
\t\t\t\t{uitest_sources_id} /* Sources */,
\t\t\t\t{uitest_frameworks_id} /* Frameworks */,
\t\t\t\t{uitest_resources_id} /* Resources */,
\t\t\t);
\t\t\tbuildRules = ();
\t\t\tdependencies = (
\t\t\t\t{uitest_dependency_id} /* PBXTargetDependency */,
\t\t\t);
\t\t\tname = GoogleInterviewPrepUITests;
\t\t\tproductName = GoogleInterviewPrepUITests;
\t\t\tproductReference = {uitest_product_fileref} /* GoogleInterviewPrepUITests.xctest */;
\t\t\tproductType = "com.apple.product-type.bundle.ui-testing";
\t\t}};
"""

# Project Object
project_obj_id = gen_id("PROJECT")
project_object = f"""
\t\t{project_obj_id} /* Project object */ = {{
\t\t\tisa = PBXProject;
\t\t\tattributes = {{
\t\t\t\tBuildIndependentTargetsInParallel = 1;
\t\t\t\tLastUpgradeCheck = 1500;
\t\t\t\tTargetAttributes = {{
\t\t\t\t\t{app_target_id} = {{
\t\t\t\t\t\tCreatedOnToolsVersion = 15.0;
\t\t\t\t\t}};
\t\t\t\t\t{test_target_id} = {{
\t\t\t\t\t\tCreatedOnToolsVersion = 15.0;
\t\t\t\t\t\tTestTargetID = {app_target_id};
\t\t\t\t\t}};
\t\t\t\t\t{uitest_target_id} = {{
\t\t\t\t\t\tCreatedOnToolsVersion = 15.0;
\t\t\t\t\t\tTestTargetID = {app_target_id};
\t\t\t\t\t}};
\t\t\t\t}};
\t\t\t}};
\t\t\tbuildConfigurationList = {proj_cfg_list} /* Build configuration list for PBXProject */;
\t\t\tcompatibilityVersion = "Xcode 14.0";
\t\t\tdevelopmentRegion = en;
\t\t\thasScannedForEncodings = 0;
\t\t\tknownRegions = (
\t\t\t\ten,
\t\t\t\tBase,
\t\t\t);
\t\t\tmainGroup = {root_group_id};
\t\t\tproductRefGroup = {products_group_id} /* Products */;
\t\t\tprojectDirPath = "";
\t\t\tprojectRoot = "";
\t\t\ttargets = (
\t\t\t\t{app_target_id} /* GoogleInterviewPrep */,
\t\t\t\t{test_target_id} /* GoogleInterviewPrepTests */,
\t\t\t\t{uitest_target_id} /* GoogleInterviewPrepUITests */,
\t\t\t);
\t\t}};
"""

# Full PBXProj assembly
pbx_content = f"""// !$*UTF8*$!
{{
\tarchiveVersion = 1;
\tclasses = {{
\t}};
\tobjectVersion = 56;
\tobjects = {{

/* Begin PBXBuildFile section */
{chr(10).join(pbx_buildfiles)}
/* End PBXBuildFile section */

/* Begin PBXContainerItemProxy section */
{dependencies}
/* End PBXContainerItemProxy section */

/* Begin PBXFileReference section */
{chr(10).join(pbx_filerefs)}
/* End PBXFileReference section */

/* Begin PBXFrameworksBuildPhase section */
/* End PBXFrameworksBuildPhase section */

/* Begin PBXGroup section */
{groups}
/* End PBXGroup section */

/* Begin PBXNativeTarget section */
{targets}
/* End PBXNativeTarget section */

/* Begin PBXProject section */
{project_object}
/* End PBXProject section */

/* Begin PBXResourcesBuildPhase section */
/* End PBXResourcesBuildPhase section */

/* Begin PBXSourcesBuildPhase section */
{build_phases}
/* End PBXSourcesBuildPhase section */

/* Begin XCBuildConfiguration section */
{configs}
/* End XCBuildConfiguration section */

/* Begin XCConfigurationList section */
/* End XCConfigurationList section */

\t}};
\trootObject = {project_obj_id} /* Project object */;
}}
"""

with open(f"{proj_path}/project.pbxproj", "w", encoding="utf-8") as f:
    f.write(pbx_content)
print(f"Wrote {proj_path}/project.pbxproj")

# Create Shared Scheme
scheme_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<Scheme
   LastUpgradeVersion = "1500"
   version = "1.7">
   <BuildAction
      parallelizeBuildables = "YES"
      buildImplicitDependencies = "YES">
      <BuildActionEntries>
         <BuildActionEntry
            buildForTesting = "YES"
            buildForRunning = "YES"
            buildForProfiling = "YES"
            buildForArchiving = "YES"
            buildForAnalyzing = "YES">
            <BuildableReference
               BuildableIdentifier = "primary"
               BlueprintIdentifier = "{app_target_id}"
               BuildableName = "GoogleInterviewPrep.app"
               BlueprintName = "GoogleInterviewPrep"
               ReferencedContainer = "container:GoogleInterviewPrep.xcodeproj">
            </BuildableReference>
         </BuildActionEntry>
      </BuildActionEntries>
   </BuildAction>
   <TestAction
      buildConfiguration = "Debug"
      selectedDebuggerIdentifier = "Xcode.DebuggerFoundation.Debugger.LLDB"
      selectedLauncherIdentifier = "Xcode.DebuggerFoundation.Launcher.LLDB"
      shouldUseLaunchSchemeArgsEnv = "YES">
      <Testables>
         <TestableReference
            skipped = "NO">
            <BuildableReference
               BuildableIdentifier = "primary"
               BlueprintIdentifier = "{test_target_id}"
               BuildableName = "GoogleInterviewPrepTests.xctest"
               BlueprintName = "GoogleInterviewPrepTests"
               ReferencedContainer = "container:GoogleInterviewPrep.xcodeproj">
            </BuildableReference>
         </TestableReference>
         <TestableReference
            skipped = "NO">
            <BuildableReference
               BuildableIdentifier = "primary"
               BlueprintIdentifier = "{uitest_target_id}"
               BuildableName = "GoogleInterviewPrepUITests.xctest"
               BlueprintName = "GoogleInterviewPrepUITests"
               ReferencedContainer = "container:GoogleInterviewPrep.xcodeproj">
            </BuildableReference>
         </TestableReference>
      </Testables>
   </TestAction>
   <LaunchAction
      buildConfiguration = "Debug"
      selectedDebuggerIdentifier = "Xcode.DebuggerFoundation.Debugger.LLDB"
      selectedLauncherIdentifier = "Xcode.DebuggerFoundation.Launcher.LLDB"
      launchStyle = "0"
      useCustomWorkingDirectory = "NO"
      ignoresPersistentStateOnLaunch = "NO"
      debugDocumentVersioning = "YES"
      allowLocationSimulation = "YES">
      <BuildableProductRunnable
         runnableDebuggingMode = "0">
         <BuildableReference
            BuildableIdentifier = "primary"
            BlueprintIdentifier = "{app_target_id}"
            BuildableName = "GoogleInterviewPrep.app"
            BlueprintName = "GoogleInterviewPrep"
            ReferencedContainer = "container:GoogleInterviewPrep.xcodeproj">
         </BuildableReference>
      </BuildableProductRunnable>
   </LaunchAction>
   <ProfileAction
      buildConfiguration = "Release"
      shouldUseLaunchSchemeArgsEnv = "YES"
      savedToolIdentifier = ""
      useCustomWorkingDirectory = "NO"
      debugDocumentVersioning = "YES">
      <BuildableProductRunnable
         runnableDebuggingMode = "0">
         <BuildableReference
            BuildableIdentifier = "primary"
            BlueprintIdentifier = "{app_target_id}"
            BuildableName = "GoogleInterviewPrep.app"
            BlueprintName = "GoogleInterviewPrep"
            ReferencedContainer = "container:GoogleInterviewPrep.xcodeproj">
         </BuildableReference>
      </BuildableProductRunnable>
   </ProfileAction>
   <AnalyzeAction
      buildConfiguration = "Debug">
   </AnalyzeAction>
   <ArchiveAction
      buildConfiguration = "Release"
      revealArchiveInOrganizer = "YES">
   </ArchiveAction>
</Scheme>
"""

with open(f"{schemes_dir}/GoogleInterviewPrep.xcscheme", "w", encoding="utf-8") as f:
    f.write(scheme_content)
print(f"Wrote {schemes_dir}/GoogleInterviewPrep.xcscheme")
