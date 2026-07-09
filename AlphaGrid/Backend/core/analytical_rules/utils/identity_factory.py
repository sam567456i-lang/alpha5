import uuid
import hashlib

class IdentityFactory:
    """
    Centralizes deterministic UUID generation for all DTOs and geometric elements
    to ensure reproducible replay across varied environments.
    """
    NAMESPACE_OID = uuid.NAMESPACE_OID

    @classmethod
    def generate_geometry_fingerprint(cls, price: float, timestamp: str, direction: str, timeframe: str, symbol: str) -> str:
        fingerprint_str = f"{price}|{timestamp}|{direction}|{timeframe}|{symbol}"
        return hashlib.sha256(fingerprint_str.encode('utf-8')).hexdigest()

    @classmethod
    def generate_swing_identity_id(cls, geometry_fingerprint: str, policy_checksum: str) -> str:
        return str(uuid.uuid5(cls.NAMESPACE_OID, f"swing_identity_{geometry_fingerprint}_{policy_checksum}"))

    @classmethod
    def generate_event_id(cls, event_type: str, geometry_fingerprint: str, policy_checksum: str) -> str:
        return str(uuid.uuid5(cls.NAMESPACE_OID, f"{event_type}_{geometry_fingerprint}_{policy_checksum}"))

    @classmethod
    def generate_state_id(cls, old_state_id: str, triggering_event_id: str) -> str:
        if not old_state_id:
            return str(uuid.uuid4()) # Only for very first initialization
        return str(uuid.uuid5(cls.NAMESPACE_OID, f"state_{old_state_id}_{triggering_event_id}"))

    @classmethod
    def generate_transition_id(cls, old_state_id: str, triggering_event_id: str) -> str:
        if not old_state_id:
            return str(uuid.uuid4())
        return str(uuid.uuid5(cls.NAMESPACE_OID, f"transition_{old_state_id}_{triggering_event_id}"))
