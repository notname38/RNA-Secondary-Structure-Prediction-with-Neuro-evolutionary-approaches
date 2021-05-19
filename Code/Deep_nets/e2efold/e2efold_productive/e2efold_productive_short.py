import torch.optim as optim
from torch.utils import data

from e2efold.models import ContactNetwork, ContactNetwork_test, ContactNetwork_fc
from e2efold.models import ContactAttention, ContactAttention_simple_fix_PE
from e2efold.models import Lag_PP_NN, RNA_SS_e2e, Lag_PP_zero, Lag_PP_perturb
from e2efold.models import Lag_PP_mixed, ContactAttention_simple
from e2efold.common.utils import *
from e2efold.common.config import process_config
from e2efold.evaluation import all_test_only_e2e

args = get_args()

config_file = args.config

config = process_config(config_file)
print("#####Stage 3#####")
print('Here is the configuration of this run: ')
print(config)

os.environ["CUDA_VISIBLE_DEVICES"]= config.gpu

d = config.u_net_d
BATCH_SIZE = config.BATCH_SIZE
OUT_STEP = config.OUT_STEP
LOAD_MODEL = config.LOAD_MODEL
pp_steps = config.pp_steps
pp_loss = config.pp_loss
data_type = config.data_type
model_type = config.model_type
pp_type = '{}_s{}'.format(config.pp_model, pp_steps)
rho_per_position = config.rho_per_position
e2e_model_path = '../models_ckpt/e2e_{}_{}_d{}_{}_{}_position_{}.pt'.format(model_type,
    pp_type,d, data_type, pp_loss,rho_per_position)
epoches_third = config.epoches_third
evaluate_epi = config.evaluate_epi
step_gamma = config.step_gamma
k = config.k

# if gpu is to be used
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# seed everything for reproduction
seed_torch(0)

seq_len = 600

if model_type =='test_lc':
    contact_net = ContactNetwork_test(d=d, L=seq_len).to(device)
if model_type == 'att6':
    contact_net = ContactAttention(d=d, L=seq_len).to(device)
if model_type == 'att_simple':
    contact_net = ContactAttention_simple(d=d, L=seq_len).to(device)    
if model_type == 'att_simple_fix':
    contact_net = ContactAttention_simple_fix_PE(d=d, L=seq_len, 
        device=device).to(device)
if model_type == 'fc':
    contact_net = ContactNetwork_fc(d=d, L=seq_len).to(device)
if model_type == 'conv2d_fc':
    contact_net = ContactNetwork(d=d, L=seq_len).to(device)

# need to write the class for the computational graph of lang pp
if pp_type=='nn':
    lag_pp_net = Lag_PP_NN(pp_steps, k).to(device)
if 'zero' in pp_type:
    lag_pp_net = Lag_PP_zero(pp_steps, k).to(device)
if 'perturb' in pp_type:
    lag_pp_net = Lag_PP_perturb(pp_steps, k).to(device)
if 'mixed'in pp_type:
    lag_pp_net = Lag_PP_mixed(pp_steps, k, rho_per_position).to(device)

rna_ss_e2e = RNA_SS_e2e(contact_net, lag_pp_net)

if LOAD_MODEL and os.path.isfile(e2e_model_path):
    print('Loading e2e model...')
    rna_ss_e2e.load_state_dict(torch.load(e2e_model_path))


# load test sequences
folder = config.test_folder
files = os.listdir(folder)
# files = list(filter(lambda x: 'fasta' in x, files))

sequences = list()

def load_seq(file_name):
    with open(file_name, 'r') as f:
        t = f.read()
        l = t.splitlines()
    return ''.join(l)

for file_name in files:
    sequences.append(load_seq(os.path.join(folder,file_name)))

print(sequences)
querys = list(zip(files, sequences))
querys = list(filter(lambda x: len(x[1])<=seq_len, querys))

# make the predictions

contact_net.eval()
lag_pp_net.eval()

final_result_dict = dict()

names, sequences = zip(*querys)
seq_batch = np.array_split(np.array(sequences), 
    math.ceil(len(sequences)/BATCH_SIZE))

ct_list = list()

for seqs in seq_batch:
    seq_embeddings =  list(map(seq_encoding, seqs))
    seq_embeddings = list(map(lambda x: padding(x, seq_len), 
        seq_embeddings))
    seq_embeddings = np.array(seq_embeddings)
    seq_lens = torch.Tensor(np.array(list(map(len, seqs)))).int()

    seq_embedding_batch = torch.Tensor(seq_embeddings).float().to(device)

    state_pad = torch.zeros(1,2,2).to(device)

    PE_batch = get_pe(seq_lens, seq_len).float().to(device)
    with torch.no_grad():
        pred_contacts = contact_net(PE_batch, 
            seq_embedding_batch, state_pad)
        a_pred_list = lag_pp_net(pred_contacts, seq_embedding_batch)

    # the learning pp result
    final_pred = (a_pred_list[-1].cpu()>0.5).float()
    print(final_pred.shape[0])

    for i in range(final_pred.shape[0]):
        ct_tmp = contact2ct(final_pred[i].cpu().numpy(), 
            seq_embeddings[i], seq_lens.numpy()[i])
        ct_list.append(ct_tmp)


# for saving the results
save_path = config.save_folder
if not os.path.exists(save_path):
    os.makedirs(save_path)

def save_file(folder, file, ct_contact):
        file_path = os.path.join(folder, file)
        first_line = str(len(ct_contact)) + '\t' + file + '\n'
        content = ct_contact.to_csv(header=None, index=None, sep='\t')
        with open(file_path, 'w') as f:
                f.write(first_line+content)


for i in range(len(names)):
    save_file(save_path, names[i]+'.ct', ct_list[i])
    

