import unittest
from tools.base_converter import (
    convert_bin_to_dec_hex
    , convert_dec_to_bin_hex
    , convert_hex_to_bin_dec
    , convert_q88_to_dec
    , convert_dec_to_q88
)

class TestBaseConverter(unittest.TestCase):
    ## モード 1: 2進数 → 10進/16進
    def test_mode1_signed_conversion(self):
        # 負の数 (-45) -> 0xFFD3
        dec_out, hex_out, bin_out = convert_bin_to_dec_hex("1111111111010011")
        self.assertEqual(dec_out, -45)
        self.assertEqual(hex_out, "0xFFD3")
        self.assertEqual(bin_out, "0b1111111111010011")
        # 短い入力 (15ビット) -> 32745 (正)
        dec_out, hex_out, bin_out = convert_bin_to_dec_hex("111111111101001")
        self.assertEqual(dec_out, 32745)
        self.assertEqual(hex_out, "0x7FE9")

    ## モード 2: 10進数 → 2進/16進
    def test_mode2_signed_conversion(self):
        # 負の数 (-1) -> 0xFFFF
        bin_out, hex_out = convert_dec_to_bin_hex(-1)
        self.assertEqual(bin_out, "0b1111111111111111")
        self.assertEqual(hex_out, "0xFFFF")
        # 正の数 (45) -> 0x002D
        bin_out, hex_out = convert_dec_to_bin_hex(45)
        self.assertEqual(bin_out, "0b0000000000101101")
        self.assertEqual(hex_out, "0x002D")
        # オーバーフロー (32768) -> 0x8000 (-32768) として解釈される
        bin_out, hex_out = convert_dec_to_bin_hex(32768)
        self.assertEqual(hex_out, "0x8000")

    ## モード 3: 16進数 → 2進/10進
    def test_mode3_signed_conversion(self):
        # 負の数 (0xFFD3) -> -45
        bin_out, dec_out = convert_hex_to_bin_dec("FFD3")
        self.assertEqual(dec_out, -45)
        self.assertEqual(bin_out, "0b1111111111010011")
        # 正の数 (0x1234) -> 4660
        bin_out, dec_out = convert_hex_to_bin_dec("1234")
        self.assertEqual(dec_out, 4660)
        self.assertEqual(bin_out, "0b0001001000110100")

    ## モード 4: 16進 固定小数点 (8.8) → 10進
    def test_mode4_q88_to_dec(self):
        # 正の値 (0x1080) -> 16.5
        dec_out, int_p, frac_int, frac = convert_q88_to_dec("1080")
        self.assertAlmostEqual(dec_out, 16.5) # 小数点を含むため assertAlmostEqual
        self.assertEqual(int_p, 16)
        self.assertEqual(frac_int, 128)
        # 負の値 (0xBF00) -> -65.0
        dec_out, int_p, frac_int, frac = convert_q88_to_dec("BF00")
        self.assertEqual(int_p, -65)
        self.assertAlmostEqual(dec_out, -65.0)
        # 最大正 (0x7FFF) -> 127.99609375
        dec_out, _, _, _ = convert_q88_to_dec("7FFF")
        self.assertAlmostEqual(dec_out, 127 + 255/256)

    ## モード 5: 10進数 → 16進 固定小数点 (8.8)
    def test_mode5_dec_to_q88(self):
        # 正の値 (16.5) -> 0x1080
        hex_out, int_p, frac_int, frac = convert_dec_to_q88(16.5)
        self.assertEqual(hex_out, "0x1080")
        self.assertEqual(int_p, 16)
        self.assertEqual(frac_int, 128)
        # 負の値 (-65.0) -> 0xBF00
        hex_out, int_p, frac_int, frac = convert_dec_to_q88(-65.0)
        self.assertEqual(hex_out, "0xBF00")
        self.assertEqual(int_p, 191) # 256 + (-65)
        # 丸め処理のテスト (1.001) -> 0x0100 (ほぼ1)
        hex_out, _, _, _ = convert_dec_to_q88(1.001)
        self.assertEqual(hex_out, "0x0100")
        # 範囲外のテスト
        hex_out, _ = convert_dec_to_q88(128.0)
        self.assertIsNone(hex_out)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
