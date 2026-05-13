# Element Templates

Copy-paste XML templates for each Draw.io element type. The `strokeColor`, `fillColor`, and `fontColor` values are placeholders — always pull actual colors from `color-palette.md` based on the element's semantic purpose.

## CRITICAL RULES FOR GENERATION

### 1. Two-Way Binding (Mandatory)
For ALL connections, you MUST perform two-way binding:
- **Arrows**: 
    - Arrow `mxCell` must have `source="source_id"` and `target="target_id"`.
- **Why**: Failure to do this causes broken connections when moving shapes.

### 2. Arrow Penetration Prevention
To prevent arrows from piercing into the shape's interior:
- **Style**: Always include `edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;` in the edge style.
- **Coordinates**: Ensure explicit entry/exit points if multiple arrows connect to the same shape side (e.g., `exitX=0.5;exitY=1;entryX=0.5;entryY=0;`).

### 3. Box Sizing (Prevent Overflow)
Use these mathematical safeguards for boxes containing text:
- Ensure `whiteSpace=wrap;html=1;` is in the style.
- **Minimums**: Never use a width smaller than 150 or a height smaller than 70 for labeled boxes. Increase `height` appropriately for multi-line text.

## Free-Floating Text (no container)
```xml
<mxCell id="label1" value="Section Title" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;fontColor=#0f172a;fontSize=20;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="30" as="geometry" />
</mxCell>
```

## Line (structural, not arrow)
```xml
<mxCell id="line1" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=2;strokeColor=#0284c7;" edge="1" parent="1">
  <mxGeometry width="50" height="50" relative="1" as="geometry">
    <mxPoint x="100" y="100" as="sourcePoint" />
    <mxPoint x="100" y="300" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

## Small Marker Dot
```xml
<mxCell id="dot1" value="" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#f0f9ff;strokeColor=#0284c7;" vertex="1" parent="1">
  <mxGeometry x="94" y="94" width="12" height="12" as="geometry" />
</mxCell>
```

## Rectangle
```xml
<mxCell id="elem1" value="Process" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f0f9ff;strokeColor=#0284c7;fontColor=#0f172a;fontSize=16;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="180" height="90" as="geometry" />
</mxCell>
```

## Arrow
```xml
<mxCell id="arrow1" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#0284c7;" edge="1" parent="1" source="elem1" target="elem2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

For curves: use waypoints with `<Array as="points">` inside `mxGeometry`.
