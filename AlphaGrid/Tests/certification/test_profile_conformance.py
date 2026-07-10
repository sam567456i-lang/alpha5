import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Backend.core.methodology.profiles.profile_loader import ProfileLoader

def test_profile_conformance():
    """
    Validates the schema and parsing of all declarative Methodology profiles.
    """
    print("Running Profile Conformance Tests...")
    
    profiles_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Backend/core/methodology/profiles'))
    loader = ProfileLoader(base_dir=profiles_dir)
    
    profiles = [f for f in os.listdir(profiles_dir) if f.endswith(".yaml") or f.endswith(".yml")]
    
    for profile_file in profiles:
        try:
            profile_data, identity = loader.load_profile(profile_file)
            assert "id" in profile_data, f"Profile {profile_file} missing 'id'"
            assert "policies" in profile_data, f"Profile {profile_file} missing 'policies'"
            assert "projections" in profile_data, f"Profile {profile_file} missing 'projections'"
            print(f"[PASS] {profile_file} parsed successfully. Identity Hash: {identity.hash}")
        except Exception as e:
            raise AssertionError(f"[FAIL] Failed to load or validate profile {profile_file}: {str(e)}")

    print(f"[PASS] All {len(profiles)} profiles conform to schema.")

if __name__ == "__main__":
    test_profile_conformance()
