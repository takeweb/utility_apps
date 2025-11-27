def convert_bin_to_dec_hex(binary_input_cleaned):
    """
    モード 1: 2進数文字列を16ビットの符号付き整数と16進数に変換するロジックを再現
    """
    bit_length = 16

    # 1. 入力文字列を16ビットにゼロ埋め (符号解釈の基準)
    padded_binary = binary_input_cleaned.zfill(bit_length)

    # 2. 16ビットの符号なし値として解釈
    decimal_output = int(padded_binary, 2)

    # 3. 2の補数として符号付き整数に変換
    if decimal_output & (1 << (bit_length - 1)):
        decimal_output -= (1 << bit_length)

    # 4. 16進数出力: 0xは小文字、値は大文字に
    hex_output = f"0x{(decimal_output & 0xFFFF):X}"

    # 2進数出力も確認のため返す
    binary_output = "0b" + padded_binary

    return decimal_output, hex_output, binary_output

def convert_dec_to_bin_hex(decimal_value):
    """
    モード 2: 10進数値を16ビットの2の補数と16進数に変換するロジックを再現
    """

    # **2の補数ロジック**：16ビットマスクを適用
    masked_value = decimal_value & 0xFFFF

    # 2進数出力: 2の補数表現で16桁固定
    binary_output = "0b" + bin(masked_value)[2:].zfill(16)

    # 16進数出力: 0xは小文字、値は大文字に
    hex_output = f"0x{masked_value:X}"

    return binary_output, hex_output

def convert_hex_to_bin_dec(hex_input_cleaned):
    """
    モード 3: 16進数文字列を2進数と10進数に変換
    """
    bit_length = 16

    # 1. 16進 -> 10進（符号付き整数として解釈）
    decimal_value = int(hex_input_cleaned, 16)

    # 2. 2の補数として符号付き整数に変換
    if decimal_value & (1 << (bit_length - 1)):
        decimal_value -= 1 << bit_length

    # 3. 10進 -> 2進
    binary_output = "0b" + bin(decimal_value & 0xFFFF)[2:].zfill(16)

    return binary_output, decimal_value

def convert_q88_to_dec(q88_hex_4digit):
    """
    モード 4: 16進 固定小数点 (8.8) を 10進 へ変換
    """
    integer_part_hex = q88_hex_4digit[0:2]
    fractional_part_hex = q88_hex_4digit[2:4]

    integer_part_dec = int(integer_part_hex, 16)
    fractional_part_dec_int = int(fractional_part_hex, 16)

    fractional_part_dec = fractional_part_dec_int / 256.0

    # 符号付き整数として解釈
    if integer_part_dec >= 128:
        integer_part_dec -= 256

    final_decimal_value = integer_part_dec + fractional_part_dec

    return final_decimal_value, integer_part_dec, fractional_part_dec_int, fractional_part_dec

def convert_dec_to_q88(decimal_value_float):
    """
    モード 5: 10進数 を 16進 固定小数点 (8.8) へ変換
    """

    if decimal_value_float < -128 or decimal_value_float >= 128:
        # この関数は範囲チェックをしない。Streamlit側で警告を出す
        return None, None

    temp_value = decimal_value_float
    if temp_value < 0:
        temp_value += 256  # 2の補数表現に変換

    integer_part = int(temp_value)
    fractional_part = temp_value - integer_part
    fractional_part_hex_int = int(round(fractional_part * 256))

    # 丸め処理によるオーバーフローを防ぐ
    if fractional_part_hex_int == 256:
        fractional_part_hex_int = 0
        integer_part += 1

    # 16進数出力: 0xは小文字、値は大文字に
    q88_hex = f"0x{integer_part:02X}{fractional_part_hex_int:02X}"

    return q88_hex, integer_part, fractional_part_hex_int, fractional_part
