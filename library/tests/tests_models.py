from django.test import TestCase

from library.models import LibraryEntry


class DemoTest(TestCase):
    def test_demo(self):
        # Comprueba que dos valores son exactamente iguales.
        self.assertEqual(4, 2+2)
        # Comprueba si una condición se cumple o no.
        self.assertTrue(4 == 4)
        self.assertFalse(5 == 4)
        # Permiten distinguir entre None y otros valores como cadenas vacías o ceros.
        self.assertIsNone(None)
        # Comprueba que una acción provoca un error concreto.
        with self.assertRaises(ZeroDivisionError):
            # Codigo que lanza la excepcion
            4/0

class LibraryEntryExternalIdLengthTests(TestCase):

    # --- Tests para el método external_id_length() ---

    def test_external_id_length_counts_regular_string(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="abc")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 3)

    def test_external_id_length_counts_empty_string_as_zero(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 0)

    def test_external_id_length_counts_whitespace(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="   ")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 3)

    def test_external_id_length_counts_max_length_boundary_100(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="x" * 100)

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 100)

    def test_external_id_length_raises_type_error_if_not_string_or_none(self):
        # Caso anómalo: asignación indebida en memoria.
        # Precondiciones
        entry = LibraryEntry(external_game_id=123)

        # Llamada
        # Comprobaciones
        with self.assertRaises(TypeError):
            entry.external_id_length()

    def test_external_id_length_counts_none_as_zero(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id=None)

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 0)

    def test_external_id_length_counts_unicode_characters(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="😀")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 1)

    def test_external_id_length_counts_multibyte_characters(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="𐍈")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 1)

    def test_external_id_length_counts_combining_characters(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="e\u0301")  # 'e' + combining acute accent

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 2)

    def test_external_id_length_counts_long_string(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="x" * 150)

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 150)

    def test_external_id_length_counts_string_with_newlines(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="line1\nline2\nline3")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 17)

    def test_external_id_length_counts_string_with_tabs(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="col1\tcol2\tcol3")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 14)
    
    def test_external_id_length_counts_string_with_mixed_characters(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="abc123!@#")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 9)

    def test_external_id_length_counts_string_with_spaces(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="   abc   ")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 9)

    def test_external_id_length_counts_asian_characters(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="漢字")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 2)

    # --- Tests para el método external_id_upper() ---

    def test_external_id_upper_converts_to_uppercase(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="abc")

        # Llamada
        resultado = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(resultado, "ABC")

    def test_external_id_upper_converts_mixed_case(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="AbC123")

        # Llamada
        resultado = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(resultado, "ABC123")

    def test_external_id_upper_converts_empty_string(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="")

        # Llamada
        resultado = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(resultado, "")

    def test_external_id_upper_converts_none_to_empty_string(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id=None)

        # Llamada
        resultado = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(resultado, "")

    def test_external_id_upper_converts_unicode_characters(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="áéí")

        # Llamada
        resultado = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(resultado, "ÁÉÍ")

    def test_external_id_upper_converts_mixed_characters(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="abc123!@#")

        # Llamada
        resultado = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(resultado, "ABC123!@#")

    def test_external_id_upper_converts_string_with_spaces(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="   abc   ")

        # Llamada
        resultado = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(resultado, "   ABC   ")

    def test_external_id_upper_converts_asian_characters(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="漢字")

        # Llamada
        resultado = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(resultado, "漢字")

    def test_external_id_upper_converts_long_string(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="x" * 150)

        # Llamada
        resultado = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(resultado, "X" * 150)

    def test_external_id_upper_converts_string_with_newlines(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="line1\nline2\nline3")

        # Llamada
        resultado = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(resultado, "LINE1\nLINE2\nLINE3")

    def test_external_id_upper_converts_string_with_tabs(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="col1\tcol2\tcol3")

        # Llamada
        resultado = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(resultado, "COL1\tCOL2\tCOL3")

    # --- Tests para el método hours_played_label() ---
    
    def test_hours_played_label_returns_none_for_zero_hours(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=0)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "none")

    def test_hours_played_label_returns_low_for_less_than_10_hours(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=5)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "low")

    def test_hours_played_label_returns_high_for_10_or_more_hours(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=15)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "high")

    def test_hours_played_label_returns_low_for_9_hours(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=9)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "low")
    
    def test_hours_played_label_returns_high_for_10_hours(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=10)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "high")

    def test_hours_played_label_returns_low_for_1_hour(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=1)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "low")

    def test_hours_played_label_returns_high_for_100_hours(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=100)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "high")

    def test_hours_played_label_returns_none_for_zero_hours_boundary(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=0)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "none")

    def test_hours_played_label_returns_low_for_just_under_10_hours(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=9)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "low")

    def test_hours_played_label_returns_high_for_just_over_10_hours(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=11)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "high")

    def test_hours_played_label_returns_none_for_large_negative_hours(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=-100)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "low") # Asumiendo que horas negativas se consideran "low"
    
    def test_hours_played_label_returns_low_for_just_1_hour(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=1)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "low")

