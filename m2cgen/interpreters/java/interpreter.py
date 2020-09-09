import os

from m2cgen import ast
from m2cgen.interpreters import mixins
from m2cgen.interpreters import utils
from m2cgen.interpreters.interpreter import ToCodeInterpreter
from m2cgen.interpreters.java.code_generator import JavaCodeGenerator


class JavaInterpreter(ToCodeInterpreter,
                      mixins.LinearAlgebraMixin,
                      mixins.SubroutinesAsFunctionsMixin):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mulVectorNumber",
    }

    exponent_function_name = "Math.exp"
    power_function_name = "Math.pow"
    tanh_function_name = "Math.tanh"
    set_contains_function_name = "contains"

    def __init__(self, package_name=None, class_name="Model", indent=4,
                 *args, **kwargs):
        self.package_name = package_name
        self.class_name = class_name
        self.indent = indent

        # We don't provide any code generator as for each subroutine we will
        # create a new one and concatenate their results into top_cg created
        # in .interpret() method.
        super().__init__(None, *args, **kwargs)

    def interpret(self, expr):
        top_cg = self.create_code_generator()

        if self.package_name:
            top_cg.add_package_name(self.package_name)

        top_cg.add_code_line("import java.util.Arrays;")
        top_cg.add_code_line("import java.util.BitSet;")

        with top_cg.class_definition(self.class_name):

            # Since we use SubroutinesAsFunctionsMixin, we already have logic
            # of adding methods. We create first subroutine for incoming
            # expression and call `process_subroutine_queue` method.
            self.enqueue_subroutine("score", expr)
            self.process_subroutine_queue(top_cg)

            if self.static_declarations:
                top_cg.add_code_line("static MinBitset {};".format(','.join([name for name, _ in self.static_declarations])))

            top_cg.add_code_line("static {")
            top_cg.increase_indent()
            top_cg.add_code_lines([line for _, line in self.static_declarations])
            top_cg.add_block_termination()
            

            if self.with_linear_algebra:
                filename = os.path.join(
                    os.path.dirname(__file__), "linear_algebra.java")
                top_cg.add_code_lines(utils.get_file_content(filename))

        return top_cg.code

    # Required by SubroutinesAsFunctionsMixin to create new code generator for
    # each subroutine.
    def create_code_generator(self):
        return JavaCodeGenerator(indent=self.indent)
