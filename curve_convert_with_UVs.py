bl_info = {
    "name": "Batch Convert Curves with UVs",
    "author": "Akhura Mazda",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object Menu",
    "description": "Converts Curves to Mesh Objects, unwrapping them with averaged edge length of UVs and placing seam",
    "category": "3D View"
}

import bpy

def main(context):
    c = bpy.context
    obj = None
    mesh = None
    bm = None
    current_area = str(bpy.context.area.ui_type)
    sel_curves_volume = []
    sel_curves_dots = []
    current_state = c.mode
    current_state_preserve = str(c.mode)
    
    if current_state == 'EDIT_CURVE' or current_state == 'EDIT_MESH':
        bpy.ops.object.mode_set(mode="OBJECT")

    for object in c.selected_objects:        
        if object.type == 'CURVE':
            data = object.data
            if data.bevel_depth or data.extrude:
                sel_curves_volume.append(object)
            else:
                sel_curves_dots.append(object)
        else:
            object.select_set(False)
    
    print(sel_curves_volume)
    print(sel_curves_dots)
    
    if sel_curves_volume:
        for curve in sel_curves_volume:
            c.view_layer.objects.active = curve
            bpy.ops.object.convert(target='MESH')
            mesh_obj = curve
            mesh_obj.data.polygons[0].select = True
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.follow_active_quads(mode='LENGTH_AVERAGE')
            bpy.ops.uv.seams_from_islands()
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode="OBJECT")
            
            print(mesh_obj, mesh_obj.type)
            
            uv_layers = mesh_obj.data.uv_layers
            active_layer = uv_layers.active
            for uv_coord in active_layer.data:
                uv_coord.uv.y -= 0.5
    
    if sel_curves_dots:
        for curve in sel_curves_dots:
            c.view_layer.objects.active = curve
            bpy.ops.object.convert(target='MESH')
    
    if current_state_preserve == 'EDIT_CURVE' or current_state_preserve == 'EDIT_MESH':
        bpy.ops.object.mode_set(mode="EDIT")

class OBJECT_OT_ConvertCurvesWithUV(bpy.types.Operator):
    """Batch Convert Curves with UVs"""
    bl_idname = "object.curve_convert_with_uvs"
    bl_label = "Convert Curves with UVs"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

def curve_convert_button(self, context):
    self.layout.operator(
        OBJECT_OT_ConvertCurvesWithUV.bl_idname,
        text="Convert Curves with UVs",
        icon='CURVE_BEZCURVE')


def register():
    bpy.utils.register_class(OBJECT_OT_ConvertCurvesWithUV)
    bpy.types.VIEW3D_MT_object_convert.append(curve_convert_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_ConvertCurvesWithUV)
    bpy.types.VIEW3D_MT_object_convert.remove(curve_convert_button)


if __name__ == "__main__":
    register()