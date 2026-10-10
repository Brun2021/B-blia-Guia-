import sys
run_number = sys.argv[1] if len(sys.argv) > 1 else "1"
p = "android/app/build.gradle"
s = open(p, encoding="utf-8").read()
signing = """    signingConfigs {
        release {
            storeFile file("release.keystore")
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias System.getenv("KEY_ALIAS")
            keyPassword System.getenv("KEY_PASSWORD")
        }
    }
    buildTypes {"""
s = s.replace("    buildTypes {", signing, 1)
s = s.replace("        release {", "        release {\n            signingConfig signingConfigs.release", 1)
s = s.replace("versionCode 1", "versionCode " + run_number, 1)
open(p, "w", encoding="utf-8").write(s)
