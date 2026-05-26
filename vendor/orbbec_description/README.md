# Orbbec Gemini335L Description Vendor

This directory vendors the Gemini335L / Gemini336L description files used by
`nero_blade_polishing`.

## Source

- Repository: `https://github.com/orbbec/OrbbecSDK_ROS2.git`
- Local source: `src/orbbec_ws/src/OrbbecSDK_ROS2/orbbec_description`
- Source branch: `v2-main`
- Source revision: `94fc83f2ac15d35b2c2d992802bdaa48289ce89a`
- `orbbec_description` version: `2.7.6`

## Vendored Files

- `urdf/gemini335L_336L.urdf.xacro`
- `meshes/gemini335L_336L/`
- `LICENSE`
- `NOTICE`

The vendored xacro keeps the official camera frame topology under
`camera_link`. The only local edit is the mesh path rewrite:

```text
package://orbbec_description/meshes/gemini335L_336L/
-> package://my_robot_description/vendor/orbbec_description/meshes/gemini335L_336L/
```

Do not add project-specific camera frames in this vendor directory. Mounting
geometry belongs in `urdf/sensors/`.
