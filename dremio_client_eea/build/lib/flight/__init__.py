# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Ryan Murray.
#
# This file is part of Dremio Client
# (see https://github.com/rymurr/dremio_client).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
try:
    import pyarrow as pa
    from pyarrow import flight
    from .flight_auth import HttpDremioClientAuthHandler

    def connect(
        hostname="localhost", port=47470, username="dremio", password="dremio123", tls_root_certs_filename=None
    ):
        """
        Connect to and authenticate against Dremio's arrow flight server. Auth is skipped if username is None

        :param hostname: Dremio coordinator hostname
        :param port: Dremio coordinator port
        :param username: Username on Dremio
        :param password: Password on Dremio
        :param tls_root_certs_filename: use ssl to connect with root certs from filename
        :return: arrow flight client
        """
        if tls_root_certs_filename:
            with open(tls_root_certs_filename) as f:
                tls_root_certs = f.read()
            location = "grpc+tls://{}:{}".format(hostname, port)
            c = flight.FlightClient(location, tls_root_certs=tls_root_certs)
        else:
            location = "grpc+tcp://{}:{}".format( hostname, port)
            c = flight.FlightClient(location)

        if username:
            c.authenticate_basic_token(username, password)

        return c

    def query(
        sql,
        client=None,
        hostname="localhost",
        port=47470,
        username="dremio",
        password="dremio123",
        pandas=True,
        tls_root_certs_filename=False,
    ):
        """
        Run an sql query against Dremio and return a pandas dataframe or arrow table

        Either host,port,user,pass tuple or a pre-connected client should be supplied. Not both

        :param sql: sql query to execute on dremio
        :param client: pre-connected client (optional)
        :param hostname: Dremio coordinator hostname (optional)
        :param port: Dremio coordinator port (optional)
        :param username: Username on Dremio (optional)
        :param password: Password on Dremio (optional)
        :param pandas: return a pandas dataframe (default) or an arrow table
        :param tls_root_certs_filename: use ssl to connect with root certs from filename
        :return:
        """
        headers = []
        headers.append((b'routing_tag', b'test-routing-tag'))
        headers.append((b'routing_queue', b'Low Cost User Queries'))

        if not client:
            client = connect(hostname, port, username, password, tls_root_certs_filename)

        bearer_token = client.authenticate_basic_token(username, password,
                                                           flight.FlightCallOptions(headers=headers))

        headers.append(bearer_token)
        flight_desc = flight.FlightDescriptor.for_command(sql)

        # Retrieve the schema of the result set.
        options = flight.FlightCallOptions(headers=headers)
        schema = client.get_schema(flight_desc, options)

        info = client.get_flight_info(flight.FlightDescriptor.for_command(sql), options)

        reader = client.do_get(info.endpoints[0].ticket, options)
        batches = []
        return reader.read_pandas()


except ImportError:

    def connect(*args, **kwargs):
        raise NotImplementedError("Python Flight bindings require Python 3 and pyarrow > 0.14.0")

    def query(*args, **kwargs):
        raise NotImplementedError("Python Flight bindings require Python 3 and pyarrow > 0.14.0")
