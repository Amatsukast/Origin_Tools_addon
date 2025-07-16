import bpy
import mathutils
from bpy.props import EnumProperty
from bpy.app.translations import pgettext_iface as _


def get_bbox_coords(obj, use_world):
    mat = obj.matrix_world if use_world else mathutils.Matrix.Identity(4)
    return [mat @ mathutils.Vector(corner) for corner in obj.bound_box]


def get_axis_minmax(obj, axis, use_world):
    coords = get_bbox_coords(obj, use_world)
    idx = "xyz".index(axis)
    values = [v[idx] for v in coords]
    return min(values), max(values)


def move_origin(
    obj, axis, to_min, use_world, center_before_move=False, move_mesh=False
):
    prev_mode = obj.mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # Center all axes first
    if center_before_move:
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_MASS")

    if move_mesh:
        # For move_mesh, use local axis and min/max only
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.origin_set(type="GEOMETRY_ORIGIN")

        idx = "xyz".index(axis)
        coords = get_bbox_coords(obj, use_world=False)
        min_val = min(v[idx] for v in coords)
        max_val = max(v[idx] for v in coords)
        target_val = min_val if to_min else max_val

        # Move mesh in opposite direction so that origin comes to target_val
        offset = -target_val
        vec = mathutils.Vector([0, 0, 0])
        vec[idx] = offset
        obj.data.transform(mathutils.Matrix.Translation(vec))
        obj.data.update()
    else:
        # Move origin (as before)
        min_val, max_val = get_axis_minmax(obj, axis, use_world)
        target_val = min_val if to_min else max_val

        cursor_prev = bpy.context.scene.cursor.location.copy()
        if use_world:
            cursor_loc = obj.matrix_world.translation.copy()
            cursor_loc[["x", "y", "z"].index(axis)] = target_val
        else:
            local_offset = [0, 0, 0]
            local_offset[["x", "y", "z"].index(axis)] = target_val
            cursor_loc = obj.matrix_world @ mathutils.Vector(local_offset)
        bpy.context.scene.cursor.location = cursor_loc
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
        bpy.context.scene.cursor.location = cursor_prev

    if prev_mode != "OBJECT":
        bpy.ops.object.mode_set(mode=prev_mode)


def get_axis_center(obj, axis, use_world):
    min_val, max_val = get_axis_minmax(obj, axis, use_world)
    return (min_val + max_val) / 2


def move_origin_center(obj, axis, use_world, center_before_move=False):
    prev_mode = obj.mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # Center all axes first
    if center_before_move:
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_MASS")

    center_val = get_axis_center(obj, axis, use_world)
    cursor_prev = bpy.context.scene.cursor.location.copy()

    if use_world:
        cursor_loc = obj.matrix_world.translation.copy()
        cursor_loc[["x", "y", "z"].index(axis)] = center_val
    else:
        local_offset = [0, 0, 0]
        local_offset[["x", "y", "z"].index(axis)] = center_val
        cursor_loc = obj.matrix_world @ mathutils.Vector(local_offset)

    bpy.context.scene.cursor.location = cursor_loc
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    bpy.context.scene.cursor.location = cursor_prev

    if prev_mode != "OBJECT":
        bpy.ops.object.mode_set(mode=prev_mode)


class ORIGINTOOLS_OT_MoveOrigin(bpy.types.Operator):
    bl_idname = "origintools.move_origin"
    bl_label = _("Move Origin")
    bl_options = {"UNDO"}  # "REGISTER" removed

    axis: EnumProperty(
        name=_("Axis"),
        description=_("The axis along which to move the origin."),
        items=[("x", "X", ""), ("y", "Y", ""), ("z", "Z", "")],
    )
    to_min: bpy.props.BoolProperty(
        name=_("To Min"), description=_("Move origin to minimum side."), default=True
    )
    use_world: bpy.props.BoolProperty(
        name=_("Use Global Axis"),
        description=_("Use global coordinates instead of local."),
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        selected = [obj for obj in context.selected_objects]
        active = context.view_layer.objects.active
        settings = context.scene.origin_tools_settings
        move_mesh = settings.move_mesh
        center_before_move = False if move_mesh else settings.center_before_move
        for obj in context.selected_objects:
            if obj.type == "MESH":
                move_origin(
                    obj,
                    self.axis,
                    self.to_min,
                    self.use_world,
                    center_before_move,
                    move_mesh,
                )
        bpy.ops.object.select_all(action="DESELECT")
        for obj in selected:
            obj.select_set(True)
        context.view_layer.objects.active = active
        return {"FINISHED"}


class ORIGINTOOLS_OT_MoveOriginCenter(bpy.types.Operator):
    bl_idname = "origintools.move_origin_center"
    bl_label = _("Move Origin to Center")
    bl_options = {"UNDO"}

    axis: EnumProperty(
        name=_("Axis"),
        description=_("The axis along which to center the origin."),
        items=[("x", "X", ""), ("y", "Y", ""), ("z", "Z", "")],
    )
    use_world: bpy.props.BoolProperty(
        name=_("Use Global Axis"),
        description=_("Use global coordinates instead of local."),
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        selected = [obj for obj in context.selected_objects]
        active = context.view_layer.objects.active
        settings = context.scene.origin_tools_settings
        move_mesh = settings.move_mesh
        center_before_move = False if move_mesh else settings.center_before_move
        for obj in context.selected_objects:
            if obj.type == "MESH":
                move_origin_center(obj, self.axis, self.use_world, center_before_move)
        bpy.ops.object.select_all(action="DESELECT")
        for obj in selected:
            obj.select_set(True)
        context.view_layer.objects.active = active
        return {"FINISHED"}


class ORIGINTOOLS_OT_MoveOriginCenterAll(bpy.types.Operator):
    bl_idname = "origintools.move_origin_center_all"
    bl_label = _("Move Origin to Center (All Axes)")
    bl_description = _(
        "Move the origin to the bounding box center or center of mass of the selected mesh objects."
    )
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        selected = [obj for obj in context.selected_objects]
        active = context.view_layer.objects.active
        move_mesh = context.scene.origin_tools_settings.move_mesh
        for obj in context.selected_objects:
            if obj.type == "MESH":
                if move_mesh:
                    bpy.ops.object.select_all(action="DESELECT")
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.origin_set(type="GEOMETRY_ORIGIN")
                    coords = get_bbox_coords(obj, use_world=False)
                    center = sum(coords, mathutils.Vector((0, 0, 0))) / 8
                    obj.data.transform(mathutils.Matrix.Translation(center))
                    obj.data.update()
                else:
                    bpy.ops.object.select_all(action="DESELECT")
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_MASS")
        bpy.ops.object.select_all(action="DESELECT")
        for obj in selected:
            obj.select_set(True)
        context.view_layer.objects.active = active
        return {"FINISHED"}


class OriginToolsSettings(bpy.types.PropertyGroup):
    axis_mode: EnumProperty(
        name=_("Axis Mode"),
        description=_("Axis reference."),
        items=[
            ("LOCAL", "Local", ""),
            ("WORLD", "Global", ""),
        ],
        default="LOCAL",
    )
    center_before_move: bpy.props.BoolProperty(
        name=_("Center Before Move"),
        description=_("Center origin on all axes before moving to specified position."),
        default=True,
    )

    def _set_move_mesh(self, value):
        self["move_mesh"] = value
        if value:
            if self.axis_mode == "WORLD":
                self.axis_mode = "LOCAL"
        # center_before_move value is not changed

    def _get_move_mesh(self):
        return self.get("move_mesh", False)

    move_mesh: bpy.props.BoolProperty(
        name=_("Move Mesh"),
        description=_("Move mesh instead of origin to match the specified position."),
        default=False,
        set=_set_move_mesh,
        get=_get_move_mesh,
    )


class ORIGINTOOLS_PT_Panel(bpy.types.Panel):
    bl_label = _("Origin Tools")
    bl_idname = "ORIGINTOOLS_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = _("Origin Tools")

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.origin_tools_settings

        # When move_mesh is enabled, gray out world axis button
        row = layout.row()
        row.enabled = not settings.move_mesh
        row.prop(settings, "axis_mode", expand=True)

        # When move_mesh is enabled, gray out center_before_move
        row = layout.row()
        row.enabled = not settings.move_mesh
        row.prop(settings, "center_before_move")

        layout.prop(settings, "move_mesh")
        use_world = settings.axis_mode == "WORLD"
        move_mesh = settings.move_mesh
        center_before_move = settings.center_before_move

        for axis in ["x", "y", "z"]:
            row = layout.row(align=True)
            row.label(text=_("{0} axis:").format(axis.upper()))

            if move_mesh:
                op = row.operator("origintools.move_origin", text=_("Min"))
                op.axis = axis
                op.to_min = True
                op.use_world = False
                op = row.operator("origintools.move_origin", text=_("Max"))
                op.axis = axis
                op.to_min = False
                op.use_world = False
            else:
                op = row.operator("origintools.move_origin", text=_("Min"))
                op.axis = axis
                op.to_min = True
                op.use_world = use_world

                # Show Center button only when center_before_move is off
                if not center_before_move:
                    op = row.operator(
                        "origintools.move_origin_center", text=_("Center")
                    )
                    op.axis = axis
                    op.use_world = use_world

                op = row.operator("origintools.move_origin", text=_("Max"))
                op.axis = axis
                op.to_min = False
                op.use_world = use_world

        layout.separator()
        layout.label(text=_("All Axes:"))
        row = layout.row()
        row.enabled = True  # Enabled regardless of move_mesh
        row.operator("origintools.move_origin_center_all", text=_("Center (All Axes)"))


classes = (
    ORIGINTOOLS_OT_MoveOrigin,
    ORIGINTOOLS_OT_MoveOriginCenter,
    ORIGINTOOLS_OT_MoveOriginCenterAll,
    ORIGINTOOLS_PT_Panel,
    OriginToolsSettings,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.origin_tools_settings = bpy.props.PointerProperty(
        type=OriginToolsSettings
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.origin_tools_settings
