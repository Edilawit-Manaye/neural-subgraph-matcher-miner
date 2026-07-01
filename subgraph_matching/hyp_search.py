def parse_encoder(parser):
    parser.opt_list('--conv_type', type=str, tunable=True, 
            options=['GIN', 'SAGE'],#, 'GCN'],#, 'GAT'],
            help='type of model')
    parser.opt_list('--skip', type=str, tunable=True, 
            options=['all', 'last'],#, 'GCN'],#, 'GAT'],
            help='type of model')
    parser.opt_list('--method_type', type=str, tunable=True,
            options=['order'],
            help='type of convolution') # can change name to embedding_type
    parser.opt_list('--order_func_grid_size', type=int, tunable=False,
            options=[1000])
    parser.opt_list('--batch_size', type=int, tunable=False,
            help='Training batch size')
    parser.opt_list('--n_layers', type=int, tunable=True, 
            options=[4, 8, 12],
            help='Number of graph conv layers')
    parser.opt_list('--hidden_dim', type=int, tunable=False,
            help='Training hidden size')
    parser.opt_list('--dropout', type=float, tunable=False,
            help='Dropout rate')
    parser.opt_list('--margin', type=float, tunable=False,
            help='margin for loss')
    parser.opt_list('--regularization', type=float, tunable=False,
            help='regularization coeff')

    # non-tunable
    parser.add_argument('--n_inner_layers', type=int,
                        help='Number of inner graph conv layers (gatedgraphconv)')
    parser.add_argument('--max_graph_size', type=int,
                        help='max training graph size')
    parser.add_argument('--n_batches', type=int,
                        help='Number of training minibatches')
    parser.add_argument('--dataset', type=str,
                        help='Dataset')
    parser.add_argument('--dataset_type', type=str,
                        help='"syn" or "real"')
    parser.add_argument('--test_set', type=str,
                        help='test set filename')
    parser.add_argument('--eval_interval', type=int,
                        help='how often to eval during training')
    parser.add_argument('--val_size', type=int,
                        help='validation set size')
    parser.add_argument('--model_path', type=str,
                        help='path to save/load model')
    parser.add_argument('--start_weights', type=str,
                        help='file to load weights from')
    parser.add_argument('--opt_scheduler', type=str,
                        help='scheduler name')
    parser.add_argument('--use_intersection', type=bool,
                        help='whether to use intersections in training')
    parser.add_argument('--use_diverse_motifs', action="store_true",
                        help='whether to use diverse motifs in training')
    parser.add_argument('--node_anchored', action="store_true",
                        help='whether to use node anchoring in training')
    parser.add_argument('--test', action="store_true")
    parser.add_argument('--n_workers', type=int)
    parser.add_argument('--tag', type=str,
        help='tag to identify the run')
    parser.add_argument('--graph_pkl_path', type=str, default=None,
                        help="Path to the .pkl file containing the graph to be used for training")
    parser.add_argument('--semantic_preset', type=str, default='biology',
                        help='Semantic synthetic preset: biology, ecommerce, or social')
    parser.add_argument('--semantic_mix_presets', type=str, default='biology,ecommerce,social',
                        help='Comma-separated presets for mixed training')
    parser.add_argument('--semantic_mix_weights', type=str, default='0.34,0.33,0.33',
                        help='Comma-separated weights for semantic_mix_presets')
    parser.add_argument('--val_semantic_preset', type=str, default='',
                        help='Optional heldout semantic preset for validation/test generation')
    parser.add_argument('--label_neg_ratio', type=float, default=0.5,
                        help='Fraction of negatives that are label-corruption negatives')
    parser.add_argument('--hard_negative_ratio', type=float, default=0.5,
                        help='Fraction of structural negatives sampled as harder near-miss negatives')
    parser.add_argument('--label_noise', type=float, default=0.05,
                        help='Label corruption rate during semantic synthetic generation')
    parser.add_argument('--use_label_features', action="store_true", default=False,
                        help='Augment node features with label_id buckets')
    parser.add_argument('--label_feature_dim', type=int, default=16,
                        help='One-hot dimension for label_id feature buckets')
    parser.add_argument('--semantic_mode', type=str, default='categorical',
                        help='Semantic feature mode: categorical or hybrid_text')
    parser.add_argument('--label_encoder_backend', type=str, default='auto',
                        help='Frozen label encoder backend: auto, sentence_transformers, cache_only, or hashing')
    parser.add_argument('--label_encoder_name', type=str, default='sentence-transformers/all-MiniLM-L6-v2',
                        help='Frozen text encoder model name when using hybrid_text mode')
    parser.add_argument('--label_encoder_cache_dir', type=str, default='artifacts/label_encoder_cache',
                        help='optional cache directory for frozen label embeddings')
    parser.add_argument('--text_encoder_dim', type=int, default=384,
                        help='Raw frozen label embedding dimension before projection')
    parser.add_argument('--text_label_dim', type=int, default=64,
                        help='Projected text-label feature dimension added to node features')
    parser.add_argument('--seed', type=int, default=42,
                        help='Global random seed')
    parser.add_argument('--order_threshold_mode', type=str, default='clf',
                        help='Prediction mode for order model: clf or margin')
    parser.add_argument('--order_margin_factor', type=float, default=0.5,
                        help='When threshold_mode=margin, classify as positive if score <= margin*factor')
    parser.add_argument('--encoder_type', type=str, default='baseline',
                        help='Graph encoder: baseline or rgcn_basis')
    parser.add_argument('--num_relations', type=int, default=64,
                        help='Maximum number of supported edge relation ids (including UNK/overflow)')
    parser.add_argument('--num_bases', type=int, default=8,
                        help='Number of basis matrices for rgcn_basis encoder')
    parser.add_argument('--rel_reg_lambda', type=float, default=1e-4,
                        help='Regularization strength for relation coefficients in rgcn_basis encoder')

    parser.set_defaults(conv_type='SAGE',
                        method_type='order',
                        dataset='syn',
                        n_layers=8,
                        batch_size=64,
                        hidden_dim=64,
                        skip="learnable",
                        dropout=0.0,
                        n_batches=1000000,
                        opt='adam',   # opt_enc_parser
                        opt_scheduler='none',
                        opt_restart=100,
                        weight_decay=0.0,
                        lr=1e-4,
                        margin=0.1,
                        test_set='',
                        eval_interval=1000,
                        n_workers=4,
                        model_path="ckpt/model.pt",
                        tag='',
                        val_size=4096,
                        node_anchored=True)
