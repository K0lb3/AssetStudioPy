from typing import List, Dict
import os
import sys

global ASSETSTUDIO_LOADED
ASSETSTUDIO_LOADED = False

ASSETSTUDIO_UTILITY_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "AssetStudioUtility"
)


def load_assetstudio():
    # we only have to import the modules once
    global ASSETSTUDIO_LOADED
    if ASSETSTUDIO_LOADED:
        return

    # try to get AssetStudioPath from environment variable
    ASSETSTUDIO_PATH = os.environ.get("AssetStudioPath", ASSETSTUDIO_UTILITY_PATH)
    if not (ASSETSTUDIO_PATH and os.path.exists(ASSETSTUDIO_PATH)):
        raise Exception(f"Couldn't find AssetStudio at \n{ASSETSTUDIO_PATH}.")

    # add the assetstudio path to the system path
    # so that pythonnet can find referenced dlls
    sys.path.append(ASSETSTUDIO_PATH)

    # set the correct runtime - in case net4 isn't used
    runtimeconfig_fp = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "runtimeconfig.json"
    )
    from clr_loader import get_coreclr
    from pythonnet import set_runtime

    set_runtime(get_coreclr(runtimeconfig_fp))

    # init pythonnet
    import clr

    # import AssetStudio
    # as the dll was created on another computer it isn't trusted by default
    # so we have to use this little workaround to load it untrusted
    from System.Reflection import Assembly

    for f in [
        "AssetStudio.dll",
        "AssetStudioUtility.dll",
    ]:
        Assembly.UnsafeLoadFrom(os.path.join(ASSETSTUDIO_PATH, f))

    # check if the assembly is loaded
    try:
        import AssetStudio
    except ImportError:
        raise ImportError("Failed to import AssetStudio")

    # 5. all good, we can set the loaded flag
    ASSETSTUDIO_LOADED = True


RuntimeMethodInfo = None


def get_class_method(clz, method_name: str) -> List[RuntimeMethodInfo]:
    """Extracts a method from a class to make it callable public via .Invoke(instance, *args)
    returns: list of methods with the given method name
    """
    import clr
    from System.Reflection import MethodInfo, BindingFlags

    return [
        x
        for x in clr.GetClrType(clz).GetMethods(
            BindingFlags.Static
            | BindingFlags.Instance
            | BindingFlags.Public
            | BindingFlags.NonPublic
        )
        if x.Name == method_name
    ]


def get_class_fields(clz) -> Dict:
    import clr
    from System.Reflection import FieldInfo, BindingFlags

    return {
        x.Name: x
        for x in clr.GetClrType(clz).GetFields(
            BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic
        )
    }


if __name__ == "__main__":
    load_assetstudio()
