[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / joinRouteSegments

# Function: joinRouteSegments()

> **joinRouteSegments**(...`segments`): `string`

Defined in: packages/bananajs/src/lib/Router/route-path.ts:12

Joins route tokens into a single Express path with a leading slash.
Empty segments are skipped. No segment should include leading/trailing slashes (use normalizeRouteToken).

## Parameters

### segments

...`string`[]

## Returns

`string`
