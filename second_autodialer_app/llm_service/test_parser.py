from utils.parser import parse_ai_response

tests = [
    # 1. Valid JSON
    {
        "input": '{"action": "call", "number": "+18005550199"}',
        "expected": {"action": "call", "number": "+18005550199", "command": None},
    },
    # 2. Plain text with phone number
    {
        "input": "Call +919876543210 please",
        "expected": {"action": "call", "number": "+919876543210", "command": None},
    },
    # 3. Random text (no number, no action)
    {
        "input": "Random text without number",
        "expected": {"action": None, "number": None, "command": None},
    },
    # 4. Invalid number inside JSON
    {
        "input": '{"number": "abc"}',
        "expected": {"action": None, "number": None, "command": None},
    },
    # 5. Call with expiry message
    {
        "input": "Call +919812345678 and tell them their subscription is about to expire.",
        "expected": {"action": "call", "number": "+919812345678", "command": "their subscription is about to expire"},
    },
    # 6. Call with delivery delay
    {
        "input": "Please call 18001234567 and inform that the delivery has been delayed.",
        "expected": {"action": "call", "number": "+18001234567", "command": "the delivery has been delayed"},
    },
    # 7. Call with insurance verification
    {
        "input": "Make a call to +14155552671 and say that the insurance verification is complete.",
        "expected": {"action": "call", "number": "+14155552671", "command": "the insurance verification is complete"},
    },
    # 8. Call with payment reminder
    {
        "input": "Dial +447911123456 and remind the client about their payment due tomorrow.",
        "expected": {"action": "call", "number": "+447911123456", "command": "their payment due tomorrow"},
    },
    # 9. Call with KYC approved message
    {
        "input": "Call up 18005551234 ASAP — message: Your KYC has been successfully approved.",
        "expected": {"action": "call", "number": "+18005551234", "command": "Your KYC has been successfully approved"},
    },
]

print("Running parse_ai_response() tests...\n")

for idx, t in enumerate(tests, 1):
    output = parse_ai_response(t["input"])
    passed = output == t["expected"]

    print(f"Test {idx}: {t['input']}")
    print(f" → Output:   {output}")
    print(f" → Expected: {t['expected']}")
    print(f" ✅ PASS\n" if passed else f" ❌ FAIL\n")
