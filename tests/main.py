import unittest

if __name__ == '__main__':
    # Ejecuta todas las pruebas en este directorio y todos los inferiores
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir)

    # Ejecuta las pruebas
    runner = unittest.TextTestRunner()
    runner.run(suite)
