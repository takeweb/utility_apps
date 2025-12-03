import ipaddress


def calculate_subnet_mask(prefix_length):
    """
    サブネットマスクの計算関数
    Args:
        prefix_length (int): CIDR表記のプレフィックス長 (例: 24)
    Returns:
        tuple: (binary_mask (str), decimal_mask (str))
    """
    # 2進数表現
    binary_mask = "1" * prefix_length + "0" * (32 - prefix_length)
    binary_mask_formatted = " ".join([binary_mask[i : i + 8] for i in range(0, 32, 8)])

    # 10進数表現
    decimal_mask = str(ipaddress.IPv4Address(int(binary_mask, 2)))

    return binary_mask_formatted, decimal_mask
