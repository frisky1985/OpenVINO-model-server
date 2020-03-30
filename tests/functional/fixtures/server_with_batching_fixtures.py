#
# Copyright (c) 2019 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import pytest
from utils.model_management import wait_endpoint_setup
from utils.parametrization import get_ports_prefixes, get_tests_suffix


@pytest.fixture(scope="class")
def start_server_batch_model(request, get_image, get_test_dir,
                             get_docker_context):
    client = get_docker_context
    path_to_mount = get_test_dir + '/saved_models/'
    volumes_dict = {'{}'.format(path_to_mount): {'bind': '/opt/ml',
                                                 'mode': 'ro'}}

    ports_prefixes = get_ports_prefixes()
    suffix = "12"
    ports = {"grpc_port": int(ports_prefixes["grpc_port_prefix"]+suffix),
             "rest_port": int(ports_prefixes["rest_port_prefix"]+suffix)}
    grpc_port, rest_port = ports["grpc_port"], ports["rest_port"]

    command = "/ie-serving-py/start_server.sh ie_serving model " \
              "--model_name resnet --model_path /opt/ml/resnet_V1_50_batch8 " \
              "--port {} --rest_port {}".format(grpc_port, rest_port)

    container = client.containers.run(image=get_image, detach=True,
                                      name='ie-serving-py-test-batch-{}'.
                                      format(get_tests_suffix()),
                                      ports={'{}/tcp'.format(grpc_port):
                                             grpc_port,
                                             '{}/tcp'.format(rest_port):
                                             rest_port},
                                      remove=True, volumes=volumes_dict,
                                      command=command)
    request.addfinalizer(container.kill)

    running = wait_endpoint_setup(container)
    assert running is True, "docker container was not started successfully"

    return container, ports


@pytest.fixture(scope="class")
def start_server_batch_model_2out(request, get_image, get_test_dir,
                                  get_docker_context):
    client = get_docker_context
    path_to_mount = get_test_dir + '/saved_models/'
    volumes_dict = {'{}'.format(path_to_mount): {'bind': '/opt/ml',
                                                 'mode': 'ro'}}
    ports_prefixes = get_ports_prefixes()
    suffix = "13"
    ports = {"grpc_port": int(ports_prefixes["grpc_port_prefix"]+suffix),
             "rest_port": int(ports_prefixes["rest_port_prefix"]+suffix)}
    grpc_port, rest_port = ports["grpc_port"], ports["rest_port"]

    command = "/ie-serving-py/start_server.sh ie_serving model " \
              "--model_name age_gender " \
              "--model_path /opt/ml/age-gender-recognition-retail-0013 " \
              "--port {} --rest_port {}".format(grpc_port, rest_port)

    container = client.containers.run(image=get_image, detach=True,
                                      name='ie-serving-py-test-batch-2out-{}'.
                                      format(get_tests_suffix()),
                                      ports={'{}/tcp'.format(grpc_port):
                                             grpc_port,
                                             '{}/tcp'.format(rest_port):
                                             rest_port},
                                      remove=True, volumes=volumes_dict,
                                      command=command)
    request.addfinalizer(container.kill)

    running = wait_endpoint_setup(container)
    assert running is True, "docker container was not started successfully"

    return container, ports


@pytest.fixture(scope="class")
def start_server_batch_model_auto(request, get_image, get_test_dir,
                                  get_docker_context):
    client = get_docker_context
    path_to_mount = get_test_dir + '/saved_models/'
    volumes_dict = {'{}'.format(path_to_mount): {'bind': '/opt/ml',
                                                 'mode': 'ro'}}
    ports_prefixes = get_ports_prefixes()
    suffix = "14"
    ports = {"grpc_port": int(ports_prefixes["grpc_port_prefix"]+suffix),
             "rest_port": int(ports_prefixes["rest_port_prefix"]+suffix)}
    grpc_port, rest_port = ports["grpc_port"], ports["rest_port"]

    command = "/ie-serving-py/start_server.sh ie_serving model " \
              "--model_name resnet --model_path /opt/ml/resnet_V1_50_batch8 " \
              "--port {} --batch_size auto --rest_port {}".\
              format(grpc_port, rest_port)

    container = client.containers.run(image=get_image, detach=True,
                                      name='ie-serving-py-test-autobatch-{}'.
                                      format(get_tests_suffix()),
                                      ports={'{}/tcp'.format(grpc_port):
                                             grpc_port,
                                             '{}/tcp'.format(rest_port):
                                             rest_port},
                                      remove=True, volumes=volumes_dict,
                                      command=command)
    request.addfinalizer(container.kill)

    running = wait_endpoint_setup(container)
    assert running is True, "docker container was not started successfully"

    return container, ports


@pytest.fixture(scope="class")
def start_server_batch_model_auto_2out(request, get_image, get_test_dir,
                                       get_docker_context):
    client = get_docker_context
    path_to_mount = get_test_dir + '/saved_models/'
    volumes_dict = {'{}'.format(path_to_mount): {'bind': '/opt/ml',
                                                 'mode': 'ro'}}
    ports_prefixes = get_ports_prefixes()
    suffix = "15"
    ports = {"grpc_port": int(ports_prefixes["grpc_port_prefix"]+suffix),
             "rest_port": int(ports_prefixes["rest_port_prefix"]+suffix)}
    grpc_port, rest_port = ports["grpc_port"], ports["rest_port"]

    command = "/ie-serving-py/start_server.sh ie_serving model " \
              "--model_name age_gender " \
              "--model_path /opt/ml/age-gender-recognition-retail-0013 " \
              "--port {} --batch_size auto --rest_port {}".\
              format(grpc_port, rest_port)

    container = client.containers.run(image=get_image, detach=True,
                                      name='ie-serving-py-test-autobatch-'
                                      '2out-{}'.format(get_tests_suffix()),
                                      ports={'{}/tcp'.format(grpc_port):
                                             grpc_port,
                                             '{}/tcp'.format(rest_port):
                                             rest_port},
                                      remove=True, volumes=volumes_dict,
                                      command=command)
    request.addfinalizer(container.kill)

    running = wait_endpoint_setup(container)
    assert running is True, "docker container was not started successfully"

    return container, ports


@pytest.fixture(scope="class")
def start_server_batch_model_bs4(request, get_image, get_test_dir,
                                 get_docker_context):
    client = get_docker_context
    path_to_mount = get_test_dir + '/saved_models/'
    volumes_dict = {'{}'.format(path_to_mount): {'bind': '/opt/ml',
                                                 'mode': 'ro'}}
    ports_prefixes = get_ports_prefixes()
    suffix = "16"
    ports = {"grpc_port": int(ports_prefixes["grpc_port_prefix"]+suffix),
             "rest_port": int(ports_prefixes["rest_port_prefix"]+suffix)}
    grpc_port, rest_port = ports["grpc_port"], ports["rest_port"]

    command = "/ie-serving-py/start_server.sh ie_serving model " \
              "--model_name resnet " \
              "--model_path /opt/ml/resnet_V1_50_batch8 --port {} " \
              "--batch_size 4 --rest_port {}".format(grpc_port, rest_port)

    container = client.containers.run(image=get_image, detach=True,
                                      name='ie-serving-py-test-batch4-{}'.
                                      format(get_tests_suffix()),
                                      ports={'{}/tcp'.format(grpc_port):
                                             grpc_port,
                                             '{}/tcp'.format(rest_port):
                                             rest_port},
                                      remove=True, volumes=volumes_dict,
                                      command=command)
    request.addfinalizer(container.kill)

    running = wait_endpoint_setup(container)
    assert running is True, "docker container was not started successfully"

    return container, ports


@pytest.fixture(scope="class")
def start_server_batch_model_auto_bs4_2out(request, get_image,
                                           get_test_dir, get_docker_context):
    client = get_docker_context
    path_to_mount = get_test_dir + '/saved_models/'
    volumes_dict = {'{}'.format(path_to_mount): {'bind': '/opt/ml',
                                                 'mode': 'ro'}}

    ports_prefixes = get_ports_prefixes()
    suffix = "17"
    ports = {"grpc_port": int(ports_prefixes["grpc_port_prefix"]+suffix),
             "rest_port": int(ports_prefixes["rest_port_prefix"]+suffix)}
    grpc_port, rest_port = ports["grpc_port"], ports["rest_port"]

    command = "/ie-serving-py/start_server.sh ie_serving model " \
              "--model_name age_gender " \
              "--model_path /opt/ml/age-gender-recognition-retail-0013 " \
              "--port {} --batch_size 4 --rest_port {}".\
              format(grpc_port, rest_port)

    container = client.containers.run(image=get_image, detach=True,
                                      name='ie-serving-py-test-batch4-'
                                      '2out-{}'.format(get_tests_suffix()),
                                      ports={'{}/tcp'.format(grpc_port):
                                             grpc_port,
                                             '{}/tcp'.format(rest_port):
                                             rest_port},
                                      remove=True, volumes=volumes_dict,
                                      command=command)
    request.addfinalizer(container.kill)

    running = wait_endpoint_setup(container)
    assert running is True, "docker container was not started successfully"

    return container, ports
