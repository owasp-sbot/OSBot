from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pycallgraph import Config, GlobbingFilter, Color

from osbot.api.Lambda_Handler import Lambda_Handler
from osbot.test_helpers.Test_Data import Test_Data


class test_Lambda_Handler(TestCase):

    def setUp(self):
        self.handler = Lambda_Handler()

    def test_run(self):
        self.handler.run(Test_Data.api_gw_payload_help)

    def test_run__no_team(self):
        Dev.print(self.handler.run(Test_Data.api_gw_payload_no_team))



    # tracer tests


    def test_run_with_trace(self):
        def rainbow(node):
            return Color.hsv(node.time.fraction * 0.8, 0.4, 0.9)

        def greyscale(node):
            return Color.hsv(0, 0, node.time.fraction / 2 + 0.4)

        def orange_green(node):
            return Color( 0.2 + node.time.fraction * 0.8,
                          0.2 + node.calls.fraction * 0.4 ,
                          0.2)

        from pycallgraph.output import GraphvizOutput
        from pycallgraph import PyCallGraph

        graphviz = GraphvizOutput()
        graphviz.output_file = 'basic.png'
        graphviz.edge_color_func = lambda e: Color(0, 0, 0)
        #graphviz.node_color_func = rainbow #orange_green # greyscale

        config = Config(include_stdlib=True)#max_depth=10)
        config.trace_filter = GlobbingFilter(include=['osbot*','pbx*','boto3*'])

        with PyCallGraph(output=graphviz, config=config):
            try:
                self.handler.run(Test_Data.api_gw_payload_help)
            except Exception as error:
                Dev.pprint(error)

