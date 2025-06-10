def get_payload_template(payload: dict):
    payload_msg = """
        <p><strong>Payload:</strong></p>
        <div style="background-color: #f4f4f4; padding: 10px; border-radius: 4px;">
        """
    for key, value in payload.items():
        payload_msg += f"""
        <p style="font-weight: bold; margin: 0 0 5px 0; text-align: left;">
            {str(key).strip()}:
        </p>
        <div style="background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 10px; border-radius: 6px; 
        font-family: Consolas, 'Courier New', monospace; white-space: pre-wrap; margin-bottom: 15px;">{value}</div>
        """
    payload_msg += """
    </div>
    """
    return payload_msg
