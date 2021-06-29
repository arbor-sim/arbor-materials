import copy
import svgwrite
import math
import inputs
import seaborn
import pandas

tag_colors = ['white', '#ffc2c2', 'gray', '#c2caff']

#
# ############################################
#

def dataframe_line_plot(input_csv, output_svg):
    print('generating:', output_svg)
    dataframe = pandas.read_csv(input_csv,index_col=0)
    axes = dict(zip(['x','y','hue','col','style'],dataframe.columns.values)) # 5D seems enough for now.
    seaborn.relplot(data=dataframe, kind="line", **axes).savefig(output_svg)

#
# ############################################
#

def translate(x, f, xshift, yshift=0):
    return (f*x[0]+xshift, -f*x[1]+yshift)

def translate_all(points, f, xshift):
    return [translate(x, f, xshift) for x in points]

# Draw one or more morphologies, side by side.
# Each morphology can be drawn as segments or branches.
def morph_image(morphs, methods, filename, locset=[], sc=5):
    assert(len(morphs)==len(methods))

    print('generating:', filename)
    dwg = svgwrite.Drawing(filename=filename, debug=True)

    # Width of lines and circle strokes.
    line_width=0.1*sc

    # Padding around image.
    fudge=1.5*sc

    linecolor='black'
    pointcolor='red'
    lines = dwg.add(dwg.g(id='lines',
                          stroke=linecolor,
                          fill='white',
                          stroke_width=line_width))
    points = dwg.add(dwg.g(id='points',
                           stroke=pointcolor,
                           fill=pointcolor,
                           stroke_width=line_width))
    numbers = dwg.add(dwg.g(id='numbers',
                             text_anchor='middle',
                             alignment_baseline='middle'))

    minx = math.inf
    miny = math.inf
    maxx = -math.inf
    maxy = -math.inf

    offset = 0

    bcolor = 'mediumslateblue'
    branchfillcolor = 'lightgray'

    nmorph = len(morphs)

    for l in range(nmorph):
        morph = morphs[l]
        method = methods[l]

        nbranches = len(morph)

        segid = 0
        for i in range(nbranches):
            branch = morph[i]

            lx, ux, ly, uy = branch.minmax()
            minx = min(minx,  sc*lx+offset)
            miny = min(miny,  sc*ly)
            maxx = max(maxx,  sc*ux+offset)
            maxy = max(maxy,  sc*uy)

            if method=='segments':
                for sec in branch.sections:
                    for seg in sec:
                        if seg.length>0.00001: # only draw nonzero length segments
                            line = translate_all(seg.corners(), sc, offset)
                            lines.add(dwg.polygon(points=line, fill=tag_colors[seg.tag]))
                        segid += 1

            elif method=='branches':
                for line in branch.outline():
                    lines.add(dwg.polygon(points=translate_all(line, sc, offset),
                                          fill=branchfillcolor))

                pos = translate(branch.location(0.5), sc, offset,10)
                points.add(dwg.circle(center=pos,
                                      stroke=bcolor,
                                      r=sc*1.4,
                                      fill=bcolor))
                # The svg alignment_baseline attribute:
                #   - works on Chrome/Chromium
                #   - doesn't work on Firefox
                # so for now we just shift the relative position by sc/3
                label_pos = (pos[0], pos[1]+sc*.55)
                numbers.add(dwg.text(str(i),
                                      insert=label_pos,
                                      stroke='white',
                                      fill='white'))

            for l in range(len(locset)):
                lab = locset[l]

                # Draw the root
                root = translate(morph[0].location(0), sc, offset)
                points.add(dwg.circle(center=root, stroke='red', r=sc*0.5, fill='red'))

                if lab['type'] == 'locset':
                    for loc in lab['value']:
                        bid = loc[0]
                        pos = loc[1]

                        loc = translate(morph[bid].location(pos), sc, offset)
                        points.add(dwg.circle(center=loc, stroke='black', r=sc*0.5, fill='black'))


        offset = maxx - minx + sc


    # Find extent of image.
    minx -= fudge
    miny -= fudge
    maxx += fudge
    maxy += fudge
    width = maxx-minx
    height = maxy-miny
    dwg.viewbox(minx, -maxy, width, height)

    # Write the image to file.
    dwg.save()

# Generate an image that illustrates regions and locsets on a morphology.
#
# Can't handle morpholgies with gaps, where segemnts with a parent-child
# ordering don't have collocated distal-proximal locations respectively.
# Handling this case would make rendering regions more complex, but would
# not bee too hard to support.
def label_image(morphology, labels, filename, sc=20):
    morph = morphology
    print('generating:', filename)
    dwg = svgwrite.Drawing(filename=filename, debug=True)

    # Width of lines and circle strokes.
    line_width=0.2*sc

    # Padding around image.
    fudge=1.5*sc

    linecolor='black'
    pointcolor='red'
    lines = dwg.add(dwg.g(id='lines',
                          stroke=linecolor,
                          fill='white',
                          stroke_width=line_width))
    points = dwg.add(dwg.g(id='points',
                           stroke=pointcolor,
                           fill=pointcolor,
                           stroke_width=line_width))

    minx = math.inf
    miny = math.inf
    maxx = -math.inf
    maxy = -math.inf

    offset = 0

    branchfillcolor = 'lightgray'

    nimage = len(labels)
    for l in range(nimage):
        lab = labels[l]

        nbranches = len(morph)

        # Draw the outline of the cell
        for i in range(nbranches):
            branch = morph[i]

            lx, ux, ly, uy = branch.minmax()
            minx = min(minx,  sc*lx+offset)
            miny = min(miny,  sc*ly)
            maxx = max(maxx,  sc*ux+offset)
            maxy = max(maxy,  sc*uy)

            for line in branch.outline():
                lines.add(dwg.polygon(points=translate_all(line, sc, offset),
                                      fill=branchfillcolor,
                                      stroke=branchfillcolor))

        if lab['type'] == 'locset':
            # Draw the root
            root = translate(morph[0].location(0), sc, offset)
            points.add(dwg.circle(center=root, stroke='red', r=sc/2.5, fill='white'))

            for loc in lab['value']:
                bid = loc[0]
                pos = loc[1]

                loc = translate(morph[bid].location(pos), sc, offset)
                points.add(dwg.circle(center=loc, stroke='black', r=sc/3, fill='white'))

        if lab['type'] == 'region':
            for cab in lab['value']:
                # skip zero length cables
                bid  = cab[0]
                ppos = cab[1]
                dpos = cab[2]

                # Don't draw zero-length cables
                # How should these be drawn: with a line or a circle?
                if ppos==dpos: continue

                for line in morph[bid].outline(ppos, dpos):
                    lines.add(dwg.polygon(points=translate_all(line, sc, offset),
                                          fill='black',
                                          stroke=branchfillcolor))

        offset = maxx - minx + sc

    # Find extent of image.
    minx -= fudge
    miny -= fudge
    maxx += fudge
    maxy += fudge
    width = maxx-minx
    height = maxy-miny
    dwg.viewbox(minx, -maxy, width, height)

    # Write the image to file.
    dwg.save()

def generate(path=''):

    # morph_image([inputs.label_morph, inputs.label_morph], ['segments', 'branches'], path+'/morph_branches.svg')
    # label_image(inputs.label_morph, [inputs.ls_proxint_in, inputs.reg_proxintinf], path+'/points_region.svg')
    morph_image([inputs.label_morph], ['segments'], path+'/morph.svg')
    morph_image([inputs.label_morph], ['branches'], path+'/branches.svg',[inputs.ls_proxint_in])
    # label_image(inputs.label_morph, [inputs.ls_proxint_in], path+'/points.svg')
    label_image(inputs.label_morph, [inputs.reg_proxintinf], path+'/region.svg')

if __name__ == '__main__':
    generate('.')
