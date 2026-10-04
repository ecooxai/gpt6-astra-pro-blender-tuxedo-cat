"""Original analytic coat field shared by Python and Blender shader nodes.
No external texture or reference-image sampling is used.
"""
import math
WHITE=(.80,.779,.715);BLACK=(.0032,.0038,.0047)
class FloatOps:
 sin=staticmethod(math.sin);abs=staticmethod(abs);max=staticmethod(max)
 @staticmethod
 def clamp(x):return max(0.,min(1.,x))
 @classmethod
 def lt(cls,a,b,w):
  t=cls.clamp((b-a+w)/(2*w));return t*t*(3-2*t)
 @classmethod
 def gt(cls,a,b,w):return cls.lt(b,a,w)
def mask_field(x,y,z,op):
 ax=op.abs(x);edge=.009*op.sin(61*y+4*op.sin(29*z))+.003*op.sin(109*x+83*z)+.0025*op.sin(151*y-53*z)
 head=op.lt(((y+.965)/.485)**2+((z-1.745)/.36)**2,1+edge*2.5,.04)*op.gt(z,1.48,.008)
 width=.005+.155*op.clamp((1.945-z)/.43)**1.85
 blaze=op.lt(y,-1.04,.008)*op.lt(ax,width+edge*.2,.0035)*op.lt(z,1.935+edge*.25,.0035)
 mh=1.555-.021*op.clamp(ax/.3)+.032*op.clamp((-y-.9)/.38)
 muzzle=op.lt(z,mh+edge*.65,.006)*op.lt(y,-.73,.008);head=head*(1-blaze)*(1-muzzle)
 shoulder=((y+.31)/.255)**2+((z-1.29)/.445)**2;rump=((y-.59)/.263)**2+((z-1.27)/.322)**2
 patch=op.max(op.lt(shoulder,1+edge*7,.065),op.lt(rump,1+edge*6,.065));side=op.max(op.gt(ax,.19+edge,.006),op.gt(z,1.365,.006))
 body=patch*side*op.gt(y,-.58,.005)*op.lt(y,.92,.005)*op.gt(z,.73,.006)
 ankle=op.lt(x,-.225,.008)*op.lt(((y-.766)/.118)**2+((z-.405)/.112)**2,1+edge*4.5,.07)
 tail=op.gt(y,.86,.006)*op.gt(z,1.34+edge*.5,.008);root=op.gt(y,.80,.006)*op.lt(((x+.022)/.152)**2+((z-1.37)/.19)**2,1+edge*4,.06)
 return op.max(op.max(head,body),op.max(ankle,op.max(tail,root)))
def coat_color(p):
 b=mask_field(float(p[0]),float(p[1]),float(p[2]),FloatOps);return tuple(w+(k-w)*b for w,k in zip(WHITE,BLACK))
class NodeScalar:
 def __init__(self,ops,socket):self.ops=ops;self.socket=socket
 def __add__(self,b):return self.ops.math('ADD',self,b)
 __radd__=__add__
 def __sub__(self,b):return self.ops.math('SUBTRACT',self,b)
 def __rsub__(self,b):return self.ops.math('SUBTRACT',b,self)
 def __mul__(self,b):return self.ops.math('MULTIPLY',self,b)
 __rmul__=__mul__
 def __truediv__(self,b):return self.ops.math('DIVIDE',self,b)
 def __rtruediv__(self,b):return self.ops.math('DIVIDE',b,self)
 def __pow__(self,b):return self.ops.math('POWER',self,b)
 def __neg__(self):return self.ops.math('MULTIPLY',self,-1)
class NodeOps:
 def __init__(self,tree):self.tree=tree;self.index=0
 def math(self,kind,a,b=0):
  n=self.tree.nodes.new('ShaderNodeMath');n.operation=kind;n.location=(self.index%12*175,-self.index//12*115);self.index+=1
  for value,socket in [(a,n.inputs[0]),(b,n.inputs[1])]:
   if isinstance(value,NodeScalar):self.tree.links.new(value.socket,socket)
   else:socket.default_value=float(value)
  return NodeScalar(self,n.outputs[0])
 def sin(self,a):return self.math('SINE',a)
 def abs(self,a):return self.math('ABSOLUTE',a)
 def max(self,a,b):return self.math('MAXIMUM',a,b)
 def clamp(self,a):return self.max(0,self.math('MINIMUM',a,1))
 def lt(self,a,b,w):
  t=self.clamp((b-a+w)/(2*w));return t*t*(3-2*t)
 def gt(self,a,b,w):return self.lt(b,a,w)
def install_coat_shader(material):
 import bpy
 g=bpy.data.node_groups.new('Tuxedo pigment • original continuous 3D field','ShaderNodeTree');g.interface.new_socket(name='Rest position',in_out='INPUT',socket_type='NodeSocketVector');g.interface.new_socket(name='Color',in_out='OUTPUT',socket_type='NodeSocketColor')
 inp=g.nodes.new('NodeGroupInput');xyz=g.nodes.new('ShaderNodeSeparateXYZ');g.links.new(inp.outputs['Rest position'],xyz.inputs[0]);ops=NodeOps(g);x,y,z=[NodeScalar(ops,xyz.outputs[k]) for k in ['X','Y','Z']];mask=mask_field(x,y,z,ops)
 mix=g.nodes.new('ShaderNodeMixRGB');mix.blend_type='MIX';mix.inputs[1].default_value=(*WHITE,1);mix.inputs[2].default_value=(*BLACK,1);g.links.new(mask.socket,mix.inputs[0]);out=g.nodes.new('NodeGroupOutput');g.links.new(mix.outputs[0],out.inputs['Color'])
 n=material.node_tree.nodes;l=material.node_tree.links;attr=n.new('ShaderNodeAttribute');attr.attribute_name='CoatPosition';attr.label='Original sculpt rest coordinates';attr.location=(-600,120);field=n.new('ShaderNodeGroup');field.node_tree=g;field.location=(-300,120);l.new(attr.outputs['Vector'],field.inputs['Rest position']);l.new(field.outputs['Color'],n.get('Principled BSDF').inputs['Base Color']);return g
