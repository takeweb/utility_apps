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

    bit_length = len(binary_input_cleaned)

    # 入力文字列を bit_length ビットにゼロ埋め (符号解釈の基準)
    padded_binary = binary_input_cleaned.zfill(bit_length)

    # unsigned 値として読み取る
    decimal_unsigned = int(padded_binary, 2)

    # signed（2の補数）
    if decimal_unsigned & (1 << (bit_length - 1)):
        decimal_signed = decimal_unsigned - (1 << bit_length)
    else:
        decimal_signed = decimal_unsigned

    # -------------------------
    # HEX も bit_length に応じて可変にする
    # -------------------------
    width = (bit_length + 3) // 4  # 4bit = 1 hex、切り上げ
    mask = (1 << bit_length) - 1  # bit_length マスク
    hex = f"0x{(decimal_signed & mask):0{width}X}"

    return (decimal_signed, decimal_unsigned, hex)


def convert_dec_to_masked_value(decimal_value, bit_length):
    """
    2の補数ロジックに基づき、
    bit_lengthに合わせてマスクを作る
    """
    mask = (1 << bit_length) - 1
    masked_value = decimal_value & mask

    return masked_value


def convert_dec_to_bin(decimal_value, bit_length):
    """
    10進数値を、16ビットの2進数に変換する
    例:
    - 入力: -45 (10進数)
      出力: "0b1111111111010011" (2進数)
    - 入力: 45 (10進数)
      出力: "0b0000000000101101" (2進数)
    なお、入力が -32768 未満または 32767 超の場合はエラーとする。
    例: -40000 や 40000 はエラー。
    変換後の2進数出力は、bit_lengthで指定された桁に固定（ゼロ埋め）とする。
    例: -45 -> "0b1111111111010011", 45 -> "0b0000000000101101"
    Args:
        decimal_value (int): 変換する10進数値 (例: -45)
        bit_length (int): 2進数でのビット数 (例: 16)
    Returns:
        2進数文字列 (str)
    Raises:
        ValueError: 入力が -32768 未満または 32767 超の場合。
    """
    masked_value = convert_dec_to_masked_value(decimal_value, bit_length)

    # 2進数出力: 2の補数表現でbit_length桁固定
    binary_output = "0b" + bin(masked_value)[2:].zfill(bit_length)

    return binary_output


def convert_binary_4digit_grouping(binary_raw):
    # 先頭の「0b」を除去
    binary_without_prefix = binary_raw[2:]

    # 4桁区切りにフォーマット
    formatted_binary = " ".join(
        [
            binary_without_prefix[i : i + 4]
            for i in range(0, len(binary_without_prefix), 4)
        ]
    )

    # 先頭に「0b」を再追加
    binary_output = "0b" + formatted_binary

    return binary_output


def convert_dec_to_hex(decimal_value, bit_length):
    """
    10進数値を、16進数に変換する
    例:
    - 入力: -45 (10進数)
      出力: "0xFFD3" (16進数)
    - 入力: 45 (10進数)
      出力: "0x002D" (16進数)
    なお、入力が -32768 未満または 32767 超の場合はエラーとする。
    例: -40000 や 40000 はエラー。
    変換後の16進数出力は、bit_lengthで指定された桁固定（ゼロ埋め）で大文字とする。
    例: -45 -> "0xFFD3", 45 -> "0x002D"
    Args:
        decimal_value (int): 変換する10進数値 (例: -45)
        bit_length (int): 2進数でのビット数 (例: 16)
    Returns:
        tuple: (2進数文字列 (str), 16進数文字列 (str))
    Raises:
        ValueError: 入力が -32768 未満または 32767 超の場合。
    """
    masked_value = convert_dec_to_masked_value(decimal_value, bit_length)

    # 16進数出力:
    # - '0x' は小文字
    # - 値は f-string の書式指定で '04X' を使用
    #   - '0' : ゼロ埋め
    #   - '4' : 最小幅 4桁
    #   - 'X' : 16進数（大文字）
    width = int(bit_length / 4)
    output_hex = f"0x{masked_value:0{width}X}"

    return output_hex


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
    # 16進→10進（符号なし）
    decimal_unsigned = int(hex_input_cleaned, 16)

    # 入力HEXのビット長（4bit × 桁数）
    bit_length = len(hex_input_cleaned) * 4

    # -------------------------
    #  符号付き整数（2の補数）
    # -------------------------
    if decimal_unsigned & (1 << (bit_length - 1)):
        decimal_signed = decimal_unsigned - (1 << bit_length)
    else:
        decimal_signed = decimal_unsigned

    # -------------------------
    # 2進数出力（bit_length に合わせて可変）
    # -------------------------
    binary_output = "0b" + bin(decimal_unsigned)[2:].zfill(bit_length)

    return binary_output, decimal_signed, decimal_unsigned


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

    return (
        final_decimal_value,
        integer_part_dec,
        fractional_part_dec_int,
        fractional_part_dec,
    )


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
