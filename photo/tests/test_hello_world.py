import subprocess

def test_hello_world(capfd):
    subprocess.run(['python', 'hello_world.py'])
    captured = capfd.readouterr()
    assert captured.out == "hello world\n"
