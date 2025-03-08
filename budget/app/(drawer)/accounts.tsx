import { Stack } from 'expo-router';
import * as React from 'react';
import { View, Pressable } from 'react-native';
import { Icon } from '@roninoss/icons';
import { FlashList } from '@shopify/flash-list';

import { Container } from '~/components/Container';
import { Text } from '~/components/nativewindui/Text';
import { useColorScheme } from '~/lib/useColorScheme';

// Mock data structure for accounts
type AccountTransaction = {
  id: string;
  selected?: boolean;
  account: string;
  date: string;
  payee: string;
  category: string;
  memo: string;
  outflow?: number;
  inflow?: number;
  cleared: boolean;
};

type Column = {
  id: string;
  label?: string;
  width: string;
  align?: string;
};

// Column definitions for better maintainability
const columns: Column[] = [
  { id: 'checkbox', width: 'w-2' },
  { id: 'account', label: 'Account', width: 'w-28' },
  { id: 'date', label: 'Date', width: 'w-28' },
  { id: 'payee', label: 'Payee', width: 'w-40' },
  { id: 'category', label: 'Category', width: 'flex-1' },
  { id: 'memo', label: 'Memo', width: 'w-40' },
  { id: 'outflow', label: 'Outflow', width: 'w-28', align: 'text-right' },
  { id: 'inflow', label: 'Inflow', width: 'w-28', align: 'text-right' },
  { id: 'status', width: 'w-6' },
];

// Mock data
const mockTransactions: AccountTransaction[] = [
  {
    id: '1',
    account: 'Itau Cartão',
    date: '18/02/2025',
    payee: 'Manual Balance Adjustment',
    category: 'Inflow: Ready to Assign',
    memo: '',
    inflow: 14539.58,
    cleared: true,
  },
  // Add more mock transactions as needed
];

const TableHeader = () => (
  <View className="grid grid-cols-9 items-center border-b border-border bg-card px-3 py-4">
    {columns.map((col) => (
      <View key={col.id} className={col.width}>
        {col.label && (
          <Text className={`font-medium truncate ${col.align ?? ''}`}>
            {col.label}
          </Text>
        )}
      </View>
    ))}
  </View>
);

type TableRowProps = {
  item: AccountTransaction;
  onToggleSelect: (id: string) => void;
};

const TableRow = React.memo(({ item, onToggleSelect }: TableRowProps) => {
  const { colors } = useColorScheme();
  
  return (
    <View className="grid grid-cols-9 items-center border-b border-border bg-white dark:bg-transparent px-3 py-4 hover:bg-muted/50">
      <Pressable onPress={() => onToggleSelect(item.id)} className="w-6 items-center">
        <View className={`h-4 w-4 rounded border border-border ${item.selected ? 'bg-primary' : 'bg-transparent'}`} />
      </Pressable>
      <Text className="w-28 truncate" color="secondary">{item.account}</Text>
      <Text className="w-28" color="secondary">{item.date}</Text>
      <Text className="w-40 truncate" color="secondary">{item.payee}</Text>
      <Text className="flex-1 truncate" color="secondary">{item.category}</Text>
      <Text className="w-40 truncate" color="secondary">{item.memo}</Text>
      <Text className="w-28 text-right" color="secondary">
        {item.outflow ? `R$${item.outflow.toFixed(2)}` : ''}
      </Text>
      <Text className="w-28 text-right" color="primary">
        {item.inflow ? `R$${item.inflow.toFixed(2)}` : ''}
      </Text>
      <View className="w-6 items-center">
        {item.cleared && <Icon name="check-circle" size={16} color={colors.primary} />}
      </View>
    </View>
  );
});

TableRow.displayName = 'TableRow';

export default function Accounts() {
  const [transactions, setTransactions] = React.useState(mockTransactions);

  const toggleSelection = React.useCallback((id: string) => {
    setTransactions(prev =>
      prev.map(t =>
        t.id === id ? { ...t, selected: !t.selected } : t
      )
    );
  }, []);

  return (
    <>
      <Stack.Screen options={{ title: 'Accounts' }} />
      <Container>
        <View className="flex-1 border border-border rounded-lg overflow-hidden">
          <TableHeader />
          <FlashList
            data={transactions}
            renderItem={({ item }) => (
              <TableRow item={item} onToggleSelect={toggleSelection} />
            )}
            estimatedItemSize={56}
            keyExtractor={item => item.id}
          />
        </View>
      </Container>
    </>
  );
} 