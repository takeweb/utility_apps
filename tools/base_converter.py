def convert_bin_to_dec_hex(binary_input_cleaned):
    """
    2進数文字列を、16ビットの符号付き整数と16進数に変換する
    2の補数表現を使用。
    例:
    - 入力: "1111111111010011" (2進数で -45)
      出力: -45 (10進数), "0xFFD3" (16進数)
    - 入力: "0000000000101101" (2進数で 45)
      出力: 45 (10進数), "0x002D" (16進数)
    なお、入力が16ビット未満の場合は、左側をゼロで埋める。
    例: "1101" -> "0000000000001101"
    ただし、16ビットを超える入力はエラーとする。
    例: "11111111111111111" (17ビット) はエラー。
    変換後の16進数出力は、常に4桁固定（ゼロ埋め）で大文字とする。
    例: -45 -> "0xFFD3", 45 -> "0x002D"
    Args:
        binary_input_cleaned (str): 変換する2進数文字列 (例: "1111111111010011")
    Returns:
        tuple: (10進数値 (int), 16進数文字列 (str), 2進数文字列 (str))
    Raises:
        ValueError: 入力が16ビットを超える場合。
    """
    bit_length = 16

    # 入力文字列を16ビットにゼロ埋め (符号解釈の基準)
    padded_binary = binary_input_cleaned.zfill(bit_length)

    # 16ビットの符号なし値として解釈
    decimal_output = int(padded_binary, 2)

    # 2の補数として符号付き整数に変換
    if decimal_output & (1 << (bit_length - 1)):
        # 最上位ビット (MSB) が 1 の場合、負の値として処理
        decimal_output -= (1 << bit_length)

    # 16進数出力:
    # 16進数への変換では、元の16ビット表現 (符号なし 0xFFFF マスク) を使用
    # f-string で '04X' を使用し、4桁固定（ゼロ埋め）と大文字を指定
    hex_output = f"0x{(decimal_output & 0xFFFF):04X}"

    # 2進数出力も確認のため返す
    binary_output = "0b" + padded_binary

    return decimal_output, hex_output, binary_output

def convert_dec_to_bin_hex(decimal_value):
    """
    10進数値を、16ビットの2の補数と16進数に変換する
    例:
    - 入力: -45 (10進数)
      出力: "0b1111111111010011" (2進数), "0xFFD3" (16進数)
    - 入力: 45 (10進数)
      出力: "0b0000000000101101" (2進数), "0x002D" (16進数)
    なお、入力が -32768 未満または 32767 超の場合はエラーとする。
    例: -40000 や 40000 はエラー。
    変換後の16進数出力は、常に4桁固定（ゼロ埋め）で大文字とする。
    例: -45 -> "0xFFD3", 45 -> "0x002D"
    Args:
        decimal_value (int): 変換する10進数値 (例: -45)
    Returns:
        tuple: (2進数文字列 (str), 16進数文字列 (str))
    Raises:
        ValueError: 入力が -32768 未満または 32767 超の場合。
    """

    # **2の補数ロジック**：16ビットマスクを適用
    # 0xFFFF は 2進数で 16個の '1'
    masked_value = decimal_value & 0xFFFF

    # 2進数出力: 2の補数表現で16桁固定
    # bin() は '0b' が付くため、[2:]で削除してから zfill(16) でゼロ埋め
    binary_output = "0b" + bin(masked_value)[2:].zfill(16)

    # 16進数出力:
    # - '0x' は小文字
    # - 値は f-string の書式指定で '04X' を使用
    #   - '0' : ゼロ埋め
    #   - '4' : 最小幅 4桁
    #   - 'X' : 16進数（大文字）
    hex_output = f"0x{masked_value:04X}"

    return binary_output, hex_output

def convert_hex_to_bin_dec(hex_input_cleaned):
    """
    16進数文字列を、2進数と10進数に変換
    例:
    - 入力: "FFD3" (16進数で -45)
      出力: "0b1111111111010011" (2進数), -45 (10進数)
    - 入力: "1234" (16進数で 4660)
      出力: "0b0001001000110100" (2進数), 4660 (10進数)
    なお、入力が16ビットを超える場合はエラーとする。
    例: "1FFFF" (17ビット) はエラー。
    変換後の2進数出力は、常に16桁固定（ゼロ埋め）とする。
    例: -45 -> "0b1111111111010011", 4660 -> "0b0001001000110100"
    Args:
        hex_input_cleaned (str): 変換する16進数文字列 (例: "FFD3")
    Returns:
        tuple: (2進数文字列 (str), 10進数値 (int))
    Raises:
        ValueError: 入力が16ビットを超える場合。
    """
    bit_length = 16

    # 16進 -> 10進（符号付き整数として解釈）
    decimal_value = int(hex_input_cleaned, 16)

    # 2の補数として符号付き整数に変換
    if decimal_value & (1 << (bit_length - 1)):
        decimal_value -= 1 << bit_length

    # 10進 -> 2進
    binary_output = "0b" + bin(decimal_value & 0xFFFF)[2:].zfill(16)

    return binary_output, decimal_value

def convert_q88_to_dec(q88_hex_4digit):
    """
    16進 固定小数点 (8.8) を、10進数へ変換
    例:
    - 入力: "1080" (16進で 16.5)
      出力: 16.5 (10進数), 16 (整数部), 128 (小数部整数), 0.5 (小数部)
    - 入力: "BF00" (16進で -65.0)
      出力: -65.0 (10進数), -65 (整数部), 0 (小数部整数), 0.0 (小数部)
    なお、入力は常に4桁の16進数文字列とする。
    例: "1080", "BF00"
    Args:
        q88_hex_4digit (str): 変換する16進固定小数点(8.8)文字列 (例: "1080")
    Returns:
        tuple: (10進数値 (float), 整数部 (int), 小数部整数 (int), 小数部 (float))
    Raises:
        ValueError: 入力が4桁の16進数でない場合。
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
    10進数 を 16進 固定小数点 (8.8) へ変換
    例:
    - 入力: 16.5 (10進数)
      出力: "0x1080" (16進 固定小数点 8.8), 16 (整数部), 128 (小数部整数), 0.5 (小数部)
    - 入力: -65.0 (10進数)
      出力: "0xBF00" (16進 固定小数点 8.8), -65 (整数部), 0 (小数部整数), 0.0 (小数部)
    なお、入力値は -128 以上 128 未満とする。
    例: -130.0 や 130.0 はエラー。
    Args:
        decimal_value_float (float): 変換する10進数値 (例: 16.5)
    Returns:
        tuple: (16進数文字列 (str), 整数部 (int), 小数部整数 (int), 小数部 (float))
    Raises:
        ValueError: 入力が -128 未満または 128 以上の場合。
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
