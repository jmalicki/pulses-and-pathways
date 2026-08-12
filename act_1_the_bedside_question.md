# Act 1: The Bedside Question

**Characters:**

* **DR. SARAH HAYES**: Vascular Surgeon. Calm, experienced, and observant.
* **MARK**: Patient. Anxious oil engineer, awake, arm numb from regional anesthesia.
* **STUART**: Third-year medical student, observing the surgery.
* **ELENA**: Circulating nurse, managing IV and instruments; may call numbers from the shared vitals monitor.
* **PRIYA NAZARI**: CRNA. At the head of the table (block / MAC); usually background.

---

[*Scene Setting: Operating Room. The air is cool, hummed by the steady rhythm of the ventilation system. MARK lies supine on the operating table, his left arm extended on an armboard, prepped and draped. A screen at his shoulder hides the surgical field from his view; Dr. Hayes can look over it to meet his eyes when she speaks to him. A regional block has just been placed; they are waiting for it to set before going deeper. STUART stands beside her, observing. ELENA stands near the shared vitals monitor, adjusting the IV line. PRIYA is at the head of the table with the anesthesia machine — present, not in the light.*]


**DR. SARAH HAYES**: [*Glancing at the clock, then over the screen to Mark*] Block's in. We'll give it another minute before I go further. Okonkwo briefed me downstairs, but I want to hear it from you. While we wait—tell me what happened to your arm.

**MARK**: [*Staring at the ceiling, swallowing*] I was in the garage, using the table saw to make a cabinet with sliding glass doors. The glass was a quarter-inch thick, so I put in a quarter-inch dado set—two blades together, wide enough to cut the groove in one pass. The groove didn't go through the board. The regular guard rides on a metal fin behind the blade, and that fin had nowhere to pass, so I took the assembly off. Just for that cut. I had the wood against the guide and was using a block to push it through. It twisted; the blade threw it back. My left hand slipped, and when I jerked away, the underside of my forearm caught the cutter. I pressed the first shop rag I could reach over it and ran next door to Steve's. He drove me in.

![Accident Sketch](accident_sketch.png)

**STUART**: [*Quiet, almost to himself*] Mid-forearm… ulnar artery territory.

**DR. SARAH HAYES**: [*A short nod*] We'll see when we're in. Elena, saline ready when I ask for it.

[*She looks over the screen to Mark.*]

Mark—before I go further. I'm going to press here. Tell me: sharp, or just pressure?

[*A firm press on the forearm below the field.*]

**MARK**: [*Knuckles white on the table edge*] Not sharp. Just… weird. Like someone's rooting around in a kitchen drawer, but the drawer is my wrist.

**DR. SARAH HAYES**: [*A small nod; back to the field*] Good. That's what we want. The numbing's holding—you can feel pressure and movement, but cutting pain shouldn't get through. If anything turns sharp, say so.

**ELENA**: [*Checking the vitals monitor*] Heart rate is ninety-six, blood pressure is one-thirty-eight over eighty-two. Vitals are stable, but he's running a little fast.

**DR. SARAH HAYES**: [*Looks over the screen to Mark*] Completely normal under the circumstances. So, what is it you do, Mark?

**MARK**: [*Taking a shallow, rapid breath*] I'm an oil engineer. Reservoir and downhole hydraulics, offshore. Mostly keeping fluid columns from collapsing the rock or blowing out the top—wellbore stability, hydrostatic balance, transient pressure modeling. Math that has to work on a real well.

<!-- stage-break -->

**DR. SARAH HAYES**: [*Gently irrigating the wound with saline*] Hydrostatic balance. How does that work when you're drilling thousands of feet down?

**MARK**: [*Rambling quickly, his voice high-pitched*] It's all about density and depth. The formation rock is under immense pressure from the fluids trapped inside it. If we don't counter that pressure, the gas or oil kicks into the well, and you get a blowout. So we pump a dense drilling fluid, what we call drilling mud, down the drill pipe and up the annulus...

**STUART**: [*Frowning behind his mask*] The annulus? Like the mitral valve annulus?

**MARK**: Mitral—? I don't know what that is. In drilling, an annulus is just the empty ring-shaped space between the inner drill pipe and the outer steel casing. It's the return path. Anyway, we have to design the hydrostatic pressure to be greater than the pore pressure of the formation but less than the fracture pressure of the rock.

**STUART**: [*Leaning closer to the wound*] So the mud just sits there?

**MARK**: [*Shaking his head, staring at the ceiling*] No, it's constantly circulating. But the static base of it is just hydrostatic pressure — same rule as undergrad physics. Pressure is density times gravity times depth. Heavier mud, deeper hole, higher pressure at the bottom. If we don't control the density, the whole system destabilizes. If the mud is too light, the well kicks — sorry — formation fluid pushes into the wellbore. If it's too heavy, we fracture the reservoir and lose all our fluid into the rock, which drops the hydrostatic column and triggers a kick anyway. Same idea. It's a very tight window.

<!-- stage-break -->

> [!NOTE]
> **Hydrostatic Pressure**
> $P_h = \rho g z$
> Pressure ($P_h$) increases linearly with depth ($z$), assuming constant fluid density ($\rho$) and gravity ($g$).

**DR. SARAH HAYES**: [*Using a suction tip to clear the surgical field*] And how do you model the flow along the well? If it's circulating, it's not static anymore.

**MARK**: [*Wiggling his uninjured right hand*] Right. Once it's moving, you have to add the dynamic frictional losses. It becomes a hydrodynamic problem. Hard to talk through without a sketch. If I don't draw, I just keep thinking about what you're doing over there.

<!-- stage-break -->

**DR. SARAH HAYES**: [*Chuckles*] Stuart, let's help him out. Is there a sterile marker and a clean drape packet backing?

**STUART**: [*Retrieves a sterile skin marker and grabs a clean, stiff paper backing from a drape pack, holding it up in front of Mark's face*] Here you go, Mark. Draw it out. I'll hold it steady for you.

**MARK**: [*Takes the marker with his right hand and begins sketching rapidly on the paper backing, his hand trembling slightly but drawing clean, precise lines. He draws a concentric pipe diagram with arrows indicating flow direction*] Okay, look. This is how we visualize the system.

![The Well](01_the_well.svg)

**MARK**: [*Pointing with the marker*] Here's the physical layout. The outer boundary is the steel casing. The inner tube is the drill pipe. The mud goes down the inside of the drill pipe and comes up that gap between them we just talked about—the annulus. And the mud is thick. It's not like water. It's basically a clay slurry. It won't even start flowing until you push it hard enough, and once it does start moving, it actually thins out the faster you pump it.

<!-- stage-break -->
<!-- projections-end -->

**DR. SARAH HAYES**: [*Carefully dissecting around the ulnar artery*] So it doesn't move like water in a hose.

![Exposure Sketch](exposure_sketch.png)

<!-- stage-break -->

**MARK**: [*Nodding nervously*] Right. It moves more like a solid plug in the center, with all the shearing happening right against the walls. Plus, the drill pipe is rotating, which churns the fluid even more. When the pumps are on, the total pressure at any depth is the sum of the static weight of the fluid and the dynamic friction from pumping it.

**STUART**: [*Holding the retractor, eyes wide*] So the pressure is higher when you're pumping?

**MARK**: [*Sweat beads forming on his forehead*] Much higher. We call it the Equivalent Circulating Density, or ECD. It's the effective density the wellbore walls feel. If the ECD spikes because of high flow rates or a restriction in the annulus, we risk breaking the formation. We run computer simulations on it, breaking the whole well down into chunks. You can't just calculate it on paper because the mud gets compressed and heated the deeper it goes, changing how it flows at every single foot.

**DR. SARAH HAYES**: [*Locating the lacerated vessel, her movements precise*] There. Ulnar artery. Torn—but the ends look clean enough to work with.
