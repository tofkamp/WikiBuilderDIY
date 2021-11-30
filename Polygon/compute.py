import math
import ast
#from PIL import Image, ImageDraw

import Object2d

class Compute:
    def __init__(self, definitions):
        self.definitions = dict((d.name, d) for d in definitions)
        self.pos = (0.0, 0.0)
        self.direction = 0
        #self.img = Image.new("RGB",(1000,1700))

    def run(self):
        # execute the commands given
        # return object with shape in points
        defi = self.definitions.get('main')
        if defi is None:
            print("Cannot find 'main' definition.")
            return
        if len(defi.params) > 0:
            print("'main' definition should not have any parameters.")
            return

        self.pos = (0.0, 0.0)
        self.direction = 0
        obj = self.perform(defi.stats, {},None)

        #obj.show_image()
        return obj
        
    def perform(self, stats, variables, obj):
        if obj == None:
            obj = Object2d.Object2d()
        for stat in stats:
            if isinstance(stat, ast.LeftStat):
                #_('LEFT expr SEMI')
                #_('LEFT expr COMMA expr SEMI')
                self.direction = (self.direction + 90) % 360
                length = self.eval(stat.length, variables)
                if stat.width:
                    width = self.eval(stat.width, variables)
                else:
                    width = 0
                new_pos = self.update_pos(self.pos, self.direction, length, width)
                #self.draw(self.pos, self.direction, length, new_pos)
                self.pos = new_pos
                obj.add_border_point(self.pos)
                continue

            if isinstance(stat, ast.RightStat):
                #_('RIGHT expr SEMI')
                #_('RIGHT expr COMMA expr SEMI')
                self.direction = (self.direction + 360 - 90) % 360
                length = self.eval(stat.length, variables)
                if stat.width:
                    width = self.eval(stat.width, variables)
                else:
                    width = 0
                new_pos = self.update_pos(self.pos, self.direction, length, width)
                #self.draw(self.pos, self.direction, length, new_pos)
                self.pos = new_pos
                obj.add_border_point(self.pos)
                continue

            if isinstance(stat, ast.ForwardStat):
                #_('FORWARD expr COMMA expr SEMI')
                #_('FORWARD expr SEMI')
                length = self.eval(stat.length, variables)
                if stat.width:
                    width = self.eval(stat.width, variables)
                else:
                    width = 0
                new_pos = self.update_pos(self.pos, self.direction, length, width)
                #self.draw(self.pos, self.direction, length, new_pos)
                self.pos = new_pos
                obj.add_border_point(self.pos)
                continue
            if isinstance(stat, ast.ConnectorStat):
                #_('CONNECTOR expr COMMA expr COMMA expr COMMA expr SEMI')
                p1x = self.eval(stat.p1x, variables)
                p1y = self.eval(stat.p1y, variables)
                p2x = self.eval(stat.p2x, variables)
                p2y = self.eval(stat.p2y, variables)
                widthX = abs(p1x - p2x)
                heightY = abs(p1y - p2y)
                centroid = [(p1x + p2x) / 2,(p1y + p2y) / 2, 9]
                cd = math.cos(math.radians(self.direction))
                sd = math.sin(math.radians(self.direction))
                #obj.add_connector([self.pos[0] + p1x * sd + p1y * cd, self.pos[1] -p1x * cd + p1y * sd],
                #                  [self.pos[0] + p2x * sd + p2y * cd, self.pos[1] -p2x * cd + p2y * sd])
                obj.add_connector2([self.pos[0] + centroid[0] * sd + centroid[1] * cd, self.pos[1] - centroid[0] * cd + centroid[1] * sd, 9],
                                   widthX,heightY,self.direction)

                continue
            if isinstance(stat, ast.HoleStat):
                #_('HOLE ID AT expr COMMA expr SEMI')
                defi = self.definitions.get(stat.name)
                msg = f"Definition {stat.name} at line {stat.lineno} does not exist."
                assert defi is not None, msg
                pos = self.pos
                direction = self.direction
                self.direction = 0.0
                self.pos = (0.0, 0.0)
                hole_obj = self.perform(defi.stats, {}, None)
                self.pos = pos
                self.direction = direction
                # make sure in returned shape there is no hole defined
                # else the user wants a hole in a hole....what will that be???
                msg = f"Hole is not possible in definition {stat.name} at line {stat.lineno}."
                assert hole_obj.holes is not [], msg
                deltax = self.eval(stat.deltax, variables)
                deltay = self.eval(stat.deltay, variables)
                cd = math.cos(math.radians(self.direction))
                sd = math.sin(math.radians(self.direction))
                # move hole shape into coordinates of containig shape
                hole_obj.autoAddConnectors()
                hole_obj.moveorigin(deltax * cd + deltay * sd, -deltax * sd + deltay * cd)
                obj.add_hole(hole_obj.border)   # add outline of hole as hole
                # if there are any connectors defined in the hole, add them to the shape
                
                #obj.add_connector_boxes(hole_obj.connectors)
                obj.add_connector2_boxes(hole_obj.connectors2)
                continue
            if isinstance(stat, ast.Instantiate):
                #_('ID PAR_OPEN exprs PAR_CLOSE SEMI')
                #_('ID PAR_OPEN PAR_CLOSE SEMI')
                defi = self.definitions.get(stat.name)
                msg = f"Definition {stat.name} at line {stat.lineno} does not exist."
                assert defi is not None, msg

                if len(stat.arguments) != len(defi.params):
                    msg = f"Incorrect number of arguments while instantiating {stat.name} at line {stat.lineno}, {len(defi.params)} expected, found {len(stat.arguments)}."
                    assert False, msg

                child_vars = dict((d.name, self.eval(arg, variables)) for d, arg in zip(defi.params, stat.arguments))
                self.perform(defi.stats, child_vars,obj)
                continue

            if isinstance(stat, ast.RotateStat):
                #_('ROTATE expr SEMI')
                rotation = self.eval(stat.direction, variables)
                self.direction += rotation
                continue

            assert False, f"Unrecognized statement {stat} at {stat.lineno}."
        return obj

    def draw(self, pos, direction, length, new_pos):
        # used to draw a line so a image could be made of the shape
        # used for diagnostic and development
        # could be removed if we write .obj with connectors faces
        draw = ImageDraw.Draw(self.img)
        #print(f"draw ({pos[0]:1.1f}, {pos[1]:1.1f}) @{direction} --> ({new_pos[0]:1.1f}, {new_pos[1]:1.1f})")
        draw.line((pos[0],pos[1],new_pos[0],new_pos[1]))

    def update_pos(self, pos, direction, length, width):
        # central function to move pointer
        # in: current position, moving direction
        #     length of movement, and width (square on direction) to make skew movements
        #     without specifying the angle (with roundings errors)
        # returns the new position
        cd = math.cos(math.radians(direction))
        sd = math.sin(math.radians(direction))
        if width == 0:
            return (pos[0] + length * cd, pos[1] + length * sd)
        cw = math.cos(math.radians(direction - 90))
        sw = math.sin(math.radians(direction - 90))
        return (pos[0] + length * cd + width * cw, pos[1] + length * sd + width * sw)
        

    def eval(self, expr, variables):
        # function to calculate the result of an expression
        # returns the result value
        if isinstance(expr, ast.Subtract):
            left_val = self.eval(expr.left, variables)
            right_val = self.eval(expr.right, variables)
            return left_val - right_val

        if isinstance(expr, ast.Add):
            left_val = self.eval(expr.left, variables)
            right_val = self.eval(expr.right, variables)
            return left_val + right_val

        if isinstance(expr, ast.Multiply):
            left_val = self.eval(expr.left, variables)
            right_val = self.eval(expr.right, variables)
            return left_val * right_val

        if isinstance(expr, ast.Divide):
            left_val = self.eval(expr.left, variables)
            right_val = self.eval(expr.right, variables)
            return left_val / right_val

        if isinstance(expr, ast.Subtract):
            left_val = self.eval(expr.left, variables)
            right_val = self.eval(expr.right, variables)
            return left_val - right_val

        if isinstance(expr, ast.Negate):
            return - self.eval(expr.child, variables)

        if isinstance(expr, ast.IntLiteral):
            return expr.number

        if isinstance(expr, ast.VariableRef):
            var_val = variables.get(expr.name)
            if var_val is None:
                print(f"Variable {expr.name} at line {expr.lineno} does not exist.")
                sys.exit(1)
            return var_val

        assert False, f"Unrecognized expression {expr} at {expr.lineno}."
