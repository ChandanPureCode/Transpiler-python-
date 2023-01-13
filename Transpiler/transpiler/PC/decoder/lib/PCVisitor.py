# Generated from /antlr/PC.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .PCParser import PCParser
else:
    from PCParser import PCParser

# This class defines a complete generic visitor for a parse tree produced by PCParser.

class PCVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PCParser#dsl.
    def visitDsl(self, ctx:PCParser.DslContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PCParser#component.
    def visitComponent(self, ctx:PCParser.ComponentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PCParser#layer.
    def visitLayer(self, ctx:PCParser.LayerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PCParser#type.
    def visitType(self, ctx:PCParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PCParser#props.
    def visitProps(self, ctx:PCParser.PropsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PCParser#parentLayer.
    def visitParentLayer(self, ctx:PCParser.ParentLayerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PCParser#childLayers.
    def visitChildLayers(self, ctx:PCParser.ChildLayersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PCParser#object.
    def visitObject(self, ctx:PCParser.ObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PCParser#array.
    def visitArray(self, ctx:PCParser.ArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PCParser#pair.
    def visitPair(self, ctx:PCParser.PairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PCParser#value.
    def visitValue(self, ctx:PCParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PCParser#propReference.
    def visitPropReference(self, ctx:PCParser.PropReferenceContext):
        return self.visitChildren(ctx)



del PCParser