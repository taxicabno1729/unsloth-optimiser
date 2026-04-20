def test_dockerfile_exists():
    import os
    assert os.path.exists("Dockerfile")

def test_dockerfile_has_python():
    with open("Dockerfile") as f:
        content = f.read()
        assert "python:3.13" in content

def test_dockerfile_has_uvicorn():
    with open("Dockerfile") as f:
        content = f.read()
        assert "uvicorn" in content

def test_docker_compose_exists():
    import os
    assert os.path.exists("docker-compose.yml")

def test_docker_compose_has_services():
    import yaml
    with open("docker-compose.yml") as f:
        config = yaml.safe_load(f)
        assert "services" in config
        services = config["services"]
        assert "api" in services
        assert "worker" in services
        assert "redis" in services
        assert "postgres" in services

def test_k8s_deployment_exists():
    import os
    assert os.path.exists("k8s/deployment.yaml")

def test_k8s_service_exists():
    import os
    assert os.path.exists("k8s/service.yaml")
