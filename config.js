/* The room, read off the eight photos. Plan: the top of the plan is the window / balcony wall, so
   yaw 0 and rot 0 face it. x runs 0 (west, the bed wall) to 124 (east, the wardrobe and desk wall);
   y runs 0 (the window wall) to 134 (the door wall).

   Wall by wall, from the top-left corner, clockwise:

   TOP  (window wall, y = 0, x 0 → 124)
     0–19    plain; the skateboard leans here, a floor socket beside it
     19–65   window, 46 wide, sill 26, head 82, two sashes over two fixed lights
     (in the window's own head) the window AC, 24 × 15, its underside 67 up
     65–72   a 7″ pier
     72–100  balcony door, 28 wide, glazed to 84, a maroon curtain bunched at its east end
     100–124 the return to the corner, where the wardrobe's side stands
   RIGHT (wardrobe and desk wall, x = 124, y 0 → 134)
     0–44    wardrobe, 44 × 23 × 84, facing west, a basket and luggage on top
     44–48   a hand's gap
     48–95   desk, 47 × 23 × 30, facing west, the task chair in front of it
     ~104    the boxy wall sconce, 85 up
   BOTTOM (door wall, y = 134, x 124 → 0, i.e. right to left as you face it)
     110–124 plain
     78–110  hall door, 32 wide, the whiteboard on it, hinged on its west jamb, swings in
     69.5–78 an 8½″ pier with the light switches
     41–67   bath door, 26 wide, swings out; the skateboard deck on brackets above it
     21–41   plain
     ~20     the guitar on its winged wall mount, 38 up
     0–7     the return to the corner
   LEFT (bed wall, x = 0, y 134 → 0)
     122 → 44 the bed, head at the door end, foot toward the window
     51–105   the sun-and-moon tapestry above it, bottom edge 31 up
     44 → 0   plain

   The cameras, the two doors, the tapestry and the wardrobe were solved by least squares from
   points clicked in the photos; heights come from each photo's own ceiling and floor lines.
   ROOM.verify lists every estimate worth a tape measure. */
var CONFIG = {
  title: 'My room',
  subtitle: 'Built from eight photos · walk it, move things, add shelves',
  storageKey: 'mir-room-v1',
  accent: 0x1f4fd8, fill: 0xa6c0f6,
  view: 'se', look: 'colour',
  TEXTURES: 'textures/',
  PALETTE: {
    paint: [['Cream white', 0xf0ead9], ['Warm white', 0xf7f3ea], ['Sun ivory', 0xe8dcc0], ['Sage', 0xcbd3c2],
            ['Dusty blue', 0x93a9bf], ['Terracotta', 0xc4765a], ['Maroon', 0x6e2230], ['Charcoal', 0x33353a]],
    wood: [['Walnut door', 0x7a4e2f], ['Teak', 0x8a5a36], ['Honey', 0x9a6b3f], ['Dark brown', 0x5d4433],
           ['Hardboard', 0xc9a06a], ['Pale oak', 0xd8bb93]],
    fabric: [['Floral cream', 0xe3d2bd], ['Angry blue', 0x2f6fb5], ['Maroon velvet', 0x6e2230], ['Moss', 0x7f8c63],
             ['Night navy', 0x1b2340], ['Blush', 0xe8cfc4], ['Charcoal', 0x33353a]],
    clay: [['Terracotta pot', 0xb8704a], ['Grey stone', 0x9a9a94]]
  },
  LOOKS: [
    {name: 'As it is', colors: {}},
    {name: 'Warm white', colors: {walls: 0xf7f3ea, curtain: [0xe3d2bd, 0xb58f55], bed: [0x9a6b3f, 0xe8cfc4]}},
    {name: 'Sage', colors: {walls: 0xcbd3c2, curtain: [0xe3d2bd, 0xb58f55]}},
    {name: 'Dusty blue', colors: {walls: 0x93a9bf, curtain: [0xf0ead9, 0xb58f55], bed: [0x9a6b3f, 0xf0ead9]}}
  ],
  ROOM: {
    outline: [[0, 0], [126, 0], [126, 134], [0, 134]],
    height: 108, wall: 5,
    walls: 0xf0ead9, floor: 0xd9d6cd, trim: 0x7a4e2f,
    boards: 24, boardsDir: 'y',
    fan: {c: [61, 62], span: 48, drop: 13, blades: 3},
    openings: [
      {type: 'window', c: [46, 0], width: 46, sill: 26, head: 82, panes: 2},
      {type: 'window', c: [88, 0], width: 28, sill: 5, head: 84, panes: 1},
      {type: 'door', c: [96, 134], width: 32, hinge: 'right', swing: 'in', closed: true},
      {type: 'door', c: [54, 134], width: 26, hinge: 'left', swing: 'out', closed: true}
    ],
    fixed: [],
    verify: [
      'Room 10′-6″ × 11′-2″ (126″ × 134″) inside, scaled from the 80″ door openings and the window frame',
      'Ceiling 108″ (9 ft); the beam band above the doors is not modelled',
      'Window 46″ wide, sill 26″, head 82″, two sashes over two fixed lights, 23″ from the west corner',
      'Window AC 24 × 15 × 14, hung inside the window head, its underside 67″ up, over the window\'s west half',
      'Balcony door 28″ wide, glazed 5″ to 84″, 5″ east of the window; drawn as a tall window so its light comes in',
      'Hall door 32″ wide, bath door 26″, both 80″ high, 13″ of wall between their jambs',
      'Hall door hinged on its west jamb and swinging in — the photos do not settle which jamb',
      'Bath door swings out, into the bathroom',
      'Single bed 40 × 78, mattress 22″ up, headboard 36″, head against the door wall',
      'Bed 10″ off the door wall, its west side against the wall',
      'Wardrobe 44 × 23 × 84, with a 15″ basket of luggage on top',
      'Desk 47 × 23 × 30, standing 4″ clear of the wardrobe',
      'Tapestry 54 × 46, bottom edge 31″ up, so about 9″ of wall shows above the mattress',
      'Guitar 14″ across on its winged mount, hanging 40″ to 81″ up',
      'Skateboard deck on brackets over the bath door, 32″ wide at 80″',
      'Leaning skateboard 31″ tall, against the window wall 10″ west of the window',
      'Curtain 20″ of bunched panel, 92″ long, at the balcony door\'s east jamb',
      'Wall sconce 11 × 5½, 85″ up — high, just under the beam',
      'Door rug 30 × 18',
      'Ceiling fan 48″ sweep on a 13″ drop',
      'Floor drawn as 24″ tile courses; wall, floor and trim colours sampled from lit patches of the photos'
    ]
  },
  ITEMS: {
    bed:        {name: 'Single bed', type: 'bed', w: 40, d: 78, h: 22, hb: 36, color: 0x9a6b3f, color2: 0xe3d2bd,
                 variants: [{label: 'Yours (single)'}, {label: 'Longer', d: 84}, {label: 'Double', w: 56, d: 78}]},
    wardrobe:   {name: 'Wardrobe', type: 'wardrobe', w: 44, d: 23, h: 84, color: 0x8a5a36},
    basket:     {name: 'Basket on top', type: 'box', w: 44, d: 23, h: 15, mount: 84, color: 0x6e2230},
    desk:       {name: 'Desk', type: 'desk', w: 47, d: 23, h: 30, color: 0x5d4433, color2: 0x33353a,
                 variants: [{label: 'Yours'}, {label: 'Wider', w: 59}, {label: 'Deeper', d: 28}]},
    ac:         {name: 'Window AC', type: 'box', w: 24, d: 14, h: 15, mount: 67, color: 0xf7f3ea},
    curtain:    {name: 'Curtain', type: 'curtain', w: 20, d: 7, h: 92, mount: 0.01, color: 0x6e2230, color2: 0xb58f55},
    tapestry:   {name: 'Sun and moon tapestry', type: 'art', w: 54, d: 1.5, h: 46, mount: 31, print: 'tapestry',
                 color: 0x1b2340, color2: 0xe8dcc0},
    guitar:     {name: 'Guitar', type: 'guitar', w: 14, d: 5, h: 41, mount: 40, color: 0x6b4a94, color2: 0x2b2b2b},
    whiteboard: {name: 'Whiteboard', type: 'art', w: 26, d: 1, h: 19, mount: 42, print: 'board',
                 color: 0xf7f3ea, color2: 0x5a6b7d},
    deckshelf:  {name: 'Skateboard shelf', type: 'wallshelf', w: 32, d: 8, h: 2, mount: 80, color: 0x33353a, color2: 0x2b2b2b},
    skate:      {name: 'Skateboard', type: 'skateboard', w: 9, d: 10, h: 31, color: 0x33353a, color2: 0xc4765a},
    sconce:     {name: 'Wall sconce', type: 'sconce', w: 11, d: 4.5, h: 5.5, mount: 85, color: 0xe6e4df, color2: 0xf7f3ea},
    rug:        {name: 'Door rug', type: 'rug', w: 30, d: 18, color: 0xc4765a, color2: 0x6e2230},

    /* not in the room yet: they wait in "Add a piece" under "In this room", and option D shows them in place */
    peg:        {name: 'Pegboard', type: 'pegboard', w: 30, d: 3, h: 36, mount: 42, new: true, color: 0xc9a06a, color2: 0x5d4433,
                 variants: [{label: '30 × 36'}, {label: 'Small (24 × 24)', w: 24, h: 24}, {label: 'Wide (48 × 36)', w: 48}]},
    shelfA:     {name: 'Floating shelf', type: 'wallshelf', w: 36, d: 9, h: 2, mount: 80, new: true, color: 0xd8bb93, color2: 0x33353a,
                 variants: [{label: '3 ft'}, {label: '2 ft', w: 24}, {label: '4 ft', w: 48}]},
    shelfB:     {name: 'Shelf unit', type: 'wallshelf', w: 30, d: 10, h: 30, shelves: 3, mount: 40, new: true, color: 0xd8bb93, color2: 0x33353a,
                 variants: [{label: 'Three shelves'}, {label: 'Four shelves', shelves: 4, h: 40}, {label: 'Two shelves', shelves: 2, h: 18}]},
    bean:       {name: 'Bean bag', type: 'beanbag', w: 30, d: 30, h: 24, new: true, color: 0x7f8c63, color2: 0x7f8c63,
                 variants: [{label: 'Small'}, {label: 'Big', w: 38, d: 38, h: 30}]}
  },
  LIBRARY: [
    {id: 'peg', name: 'Pegboard', type: 'pegboard', w: 30, d: 3, h: 36, mount: 42, group: 'walls',
     variants: [{label: '30 × 36'}, {label: 'Small (24 × 24)', w: 24, h: 24}, {label: 'Wide (48 × 36)', w: 48}]},
    {id: 'shelfA', name: 'Floating shelf', type: 'wallshelf', w: 36, d: 9, h: 2, mount: 80, group: 'walls',
     variants: [{label: '3 ft'}, {label: '2 ft', w: 24}, {label: '4 ft', w: 48}]},
    {id: 'shelfB', name: 'Shelf unit', type: 'wallshelf', w: 30, d: 10, h: 30, shelves: 3, mount: 40, group: 'walls',
     variants: [{label: 'Three shelves'}, {label: 'Four shelves', shelves: 4, h: 40}, {label: 'Two shelves', shelves: 2, h: 18}]},
    {id: 'bean', name: 'Bean bag', type: 'beanbag', w: 30, d: 30, h: 24, group: 'seating',
     variants: [{label: 'Small'}, {label: 'Big', w: 38, d: 38, h: 30}]},
    {id: 'sconce2', name: 'Wall sconce', type: 'sconce', w: 11, d: 4.5, h: 5.5, mount: 85, group: 'lighting'},
    {id: 'deck2', name: 'Deck shelf', type: 'wallshelf', w: 32, d: 8, h: 2, mount: 80, group: 'walls'},
    {id: 'guitar2', name: 'Guitar on the wall', type: 'guitar', w: 14, d: 5, h: 41, mount: 40, group: 'walls'},
    {id: 'tapestry2', name: 'Tapestry', type: 'art', w: 54, d: 1.5, h: 46, mount: 31, print: 'tapestry', group: 'walls'},
    {id: 'curtain2', name: 'Curtain panel', type: 'curtain', w: 20, d: 7, h: 92, mount: 0.01, group: 'walls'}
  ],
  LAYOUTS: [
    {name: 'The room as it is',
     note: 'Everything where the photos show it: the bed down the tapestry wall with its head by the doors, the wardrobe and desk along the far wall, the middle left open. The desk looks at a blank wall and the only daylight it gets is over your shoulder.',
     place: {bed: [20, 83, 180], wardrobe: [114.5, 22, 90], basket: [114.5, 22, 90], desk: [114.5, 71.5, 90],
             ac: [25, 7, 0], curtain: [94, 3.5, 0], tapestry: [0.75, 78, 270], guitar: [20, 131.5, 180],
             whiteboard: [96, 133.5, 180], deckshelf: [54, 130, 180], skate: [6, 6, 0], sconce: [123.75, 104, 90],
             rug: [54, 118, 0]}},
    {name: 'Desk at the window',
     note: 'The desk turns to face the window for daylight and a view, the bed slides down so its head is against the door wall and the chair has room, and the wall the desk used to face takes a shelf unit and the bean bag. The trade-off is real: the desk covers the bottom of the window and narrows the walk out to the balcony.',
     place: {bed: [20, 95, 180], wardrobe: [114.5, 22, 90], basket: [114.5, 22, 90], desk: [42, 11.5, 0],
             ac: [25, 7, 0], curtain: [94, 3.5, 0], tapestry: [0.75, 90, 270], guitar: [20, 131.5, 180],
             whiteboard: [96, 133.5, 180], deckshelf: [54, 130, 180], sconce: [123.75, 104, 90],
             shelfB: [121, 84, 90], bean: [92, 76, 20], rug: [54, 118, 0]}},
    {name: 'The room the other way round',
     note: 'Bed and storage swap walls: the bed runs down the window end of the wardrobe wall with the tapestry over it, the wardrobe and desk take the old bed wall, and the walk from the hall door to the balcony is one straight run past the foot of the bed. You give up the long open middle.',
     place: {bed: [106, 48, 0], wardrobe: [11.5, 32, 270], basket: [11.5, 32, 270], desk: [11.5, 80, 270],
             ac: [25, 7, 0], curtain: [94, 3.5, 0], tapestry: [125.25, 48, 90], guitar: [20, 131.5, 180],
             whiteboard: [96, 133.5, 180], deckshelf: [54, 130, 180], skate: [5, 115, 270], sconce: [123.75, 104, 90],
             rug: [54, 118, 0]}},
    {name: 'Shelves, pegboard and a bean bag',
     note: 'The room as it is, plus the things you asked about: a pegboard and a floating shelf over the desk, a three-shelf unit over the foot of the bed, and a bean bag in the window light. Every one of them can be dragged, turned, recoloured or taken out.',
     place: {bed: [20, 83, 180], wardrobe: [114.5, 22, 90], basket: [114.5, 22, 90], desk: [114.5, 71.5, 90],
             ac: [25, 7, 0], curtain: [94, 3.5, 0], tapestry: [0.75, 78, 270], guitar: [20, 131.5, 180],
             whiteboard: [96, 133.5, 180], deckshelf: [54, 130, 180], skate: [6, 6, 0], sconce: [123.75, 104, 90],
             rug: [54, 118, 0], peg: [124.5, 71.5, 90], shelfA: [121.5, 71.5, 90], shelfB: [5, 30, 270],
             bean: [24, 28, 0]}}
  ],
  PHOTOS: [
    /* Each camera was fitted by least squares to points read off the photo (door jambs, the window
       reveals, the tapestry's edges, the wardrobe's corners, the room corners); the heights come from
       each photo's own ceiling and floor lines. Most of these are the phone's 0.5x lens, which is why
       one frame holds so much of the room; photo 6 is the 1x. Nudge any field and the model follows. */
    {src: 'photos/1-from-door.jpg',   label: 'From the hall door',       at: [105, 127], h: 50, yaw: 316, pitch: 0, roll: 0, fov: 74},
    {src: 'photos/2-to-doors.jpg',    label: 'Back toward the doors',    at: [29, 27],   h: 50, yaw: 190, pitch: 0, roll: 0, fov: 95},
    {src: 'photos/3-tapestry.jpg',    label: 'The tapestry wall',        at: [66, 75],   h: 52, yaw: 268, pitch: 0, roll: 0, fov: 91},
    {src: 'photos/4-door-wall.jpg',   label: 'The two doors',            at: [69, 62],   h: 52, yaw: 188, pitch: 0, roll: 0, fov: 92},
    {src: 'photos/5-desk-wall.jpg',   label: 'The desk wall',            at: [61, 82],   h: 56, yaw: 82,  pitch: 0, roll: 0, fov: 95},
    {src: 'photos/6-window-wall.jpg', label: 'The window wall',          at: [70, 131],  h: 60, yaw: 358, pitch: 0, roll: 0, fov: 54},
    {src: 'photos/7-from-bed.jpg',    label: 'From the head of the bed', at: [6, 119],   h: 61, yaw: 24,  pitch: 0, roll: 0, fov: 74},
    {src: 'photos/8-from-window.jpg', label: 'From the window',          at: [12, 14],   h: 50, yaw: 134, pitch: 0, roll: 0, fov: 88}
  ]
};
