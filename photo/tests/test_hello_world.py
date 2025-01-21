import subprocess


def test_hello_world_output():
    result = subprocess.run(['python', '/workspace/hello_world.py'], capture_output=True, text=True)
    assert result.stdout.strip() == 'hello world'
