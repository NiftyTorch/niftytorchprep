import os
import numpy as np

folder = 'testcopybids/'
os.mkdir(folder)
f = open(os.path.join(folder, 'participants.tsv'),'w')
f.write('participant_id\tsex\tage\n')
ages = [18, 19, 20, 30, 27, 24, 25, 44, 41, 29, 44] 
for i in range(100): 
    sex = 'M' if np.random.randint(2) else 'F' 
    np.random.shuffle(ages) 
    f.write('sub-{}\t{}\t{}\n'.format('{0:03d}'.format(i+1),sex,ages[0])) 
f.close()

json_descr = """
{
    "participant_id": {
        "LongName": "Participant ID",
        "Description": "Unique ID"
    },
    "sex": {
        "LongName": "Participant gender",
        "Description": "M or F"
    },
    "age": {
        "LongName": "Participant age",
        "Description": "yy"
    }
}
"""

with open(os.path.join(folder, 'participants.json'),'w') as ff:
    ff.write(json_descr)

for i in range(100):
    os.mkdir(folder+'sub-{0:03d}'.format(i+1))
    os.mkdir(folder+'sub-{0:03d}/anat'.format(i+1))
    os.mkdir(folder+'sub-{0:03d}/func'.format(i+1))
    open(folder+'sub-{0:03d}/anat/sub-{0:03d}_t1.nii.gz'.format(i+1, i+1), 'a').close()
    open(folder+'sub-{0:03d}/func/sub-{0:03d}_task.nii.gz'.format(i+1, i+1), 'a').close()
