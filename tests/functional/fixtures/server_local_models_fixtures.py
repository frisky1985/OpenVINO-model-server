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

import shutil
import os
import pytest
from utils.model_management import wait_endpoint_setup
from utils.parametrization import get_ports_prefixes, get_tests_suffix


@pytest.fixture(scope="class")
def start_server_single_model(request, get_image, get_test_dir,
                              get_docker_context):

    client = get_docker_context
    path_to_mount = get_test_dir + '/saved_models/'
    volumes_dict = {'{}'.format(path_to_mount): {'bind': '/opt/ml',
                                                 'mode': 'ro'}}

    ports_prefixes = get_ports_prefixes()
    suffix = "05"
    ports = {"grpc_port": int(ports_prefixes["grpc_port_prefix"]+suffix),
             "rest_port": int(ports_prefixes["rest_port_prefix"]+suffix)}
    grpc_port, rest_port = ports["grpc_port"], ports["rest_port"]

    command = "/ie-serving-py/start_server.sh ie_serving model " \
              "--model_name resnet " \
              "--model_path /opt/ml/resnet_V1_50 " \
              "--port " + str(grpc_port) + " --rest_port " + str(rest_port) + \
              " --plugin_config " \
              "\"{\\\"CPU_THROUGHPUT_STREAMS\\\": " \
              "\\\"CPU_THROUGHPUT_AUTO\\\"}\""

    container = \
        client.containers.run(
            image=get_image,
            detach=True,
            name='ie-serving-py-test-single-{}'.format(get_tests_suffix()),
            ports={'{}/tcp'.format(grpc_port): grpc_port,
                   '{}/tcp'.format(rest_port): rest_port},
            remove=True,
            volumes=volumes_dict,
            # In this case, slower,
            # non-default serialization method is used
            environment=[
                'SERIALIZATON=_prepare_output_as_AppendArrayToTensorProto'],
            command=command)
    request.addfinalizer(container.kill)

    running = wait_endpoint_setup(container)
    assert running is True, "docker container was not started successfully"

    return container, ports


@pytest.fixture(scope="class")
def start_server_with_mapping(request, get_image, get_test_dir,
                              get_docker_context):
    shutil.copyfile('tests/functional/mapping_config.json',
                    get_test_dir + '/saved_models/'
                                   'age-gender-recognition-retail-0013/1/'
                                   'mapping_config.json')
    client = get_docker_context
    path_to_mount = get_test_dir + '/saved_models/'
    volumes_dict = {'{}'.format(path_to_mount): {'bind': '/opt/ml',
                                                 'mode': 'ro'}}

    ports_prefixes = get_ports_prefixes()
    suffix = "06"
    ports = {"grpc_port": int(ports_prefixes["grpc_port_prefix"]+suffix),
             "rest_port": int(ports_prefixes["rest_port_prefix"]+suffix)}
    grpc_port, rest_port = ports["grpc_port"], ports["rest_port"]

    command = "/ie-serving-py/start_server.sh ie_serving model " \
              "--model_name age_gender " \
              "--model_path /opt/ml/age-gender-recognition-retail-0013 " \
              "--port {} --rest_port {}".format(grpc_port, rest_port)

    container = client.containers.run(image=get_image, detach=True,
                                      name='ie-serving-py-test-2-out-{}'.
                                      format(get_tests_suffix()),
                                      ports={'{}/tcp'.format(grpc_port):
                                             grpc_port,
                                             '{}/tcp'.format(rest_port):
                                             rest_port},
                                      remove=True, volumes=volumes_dict,
                                      command=command)

    def delete_mapping_file():
        path = get_test_dir + '/saved_models/' \
                              'age-gender-recognition-retail-0013/1/' \
                              'mapping_config.json'
        if os.path.exists(path):
            os.remove(path)

    request.addfinalizer(delete_mapping_file)
    request.addfinalizer(container.kill)

    running = wait_endpoint_setup(container)
    assert running is True, "docker container was not started successfully"

    return container, ports
